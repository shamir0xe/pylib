import threading
import traceback
from typing import Callable, Dict, List
import logging
import json
import functools

from pika import BasicProperties
from pika.channel import Channel
from pika.frame import Method
from .rpc_async_connection import RpcAsyncConnection

LOGGER = logging.getLogger(__name__)
LOG_MAX_LENGTH = 222


class RpcAsyncServer:
    connection: RpcAsyncConnection
    routing_key: str
    query_handler: Callable[[Dict], str]
    channel: Channel
    threads: List[threading.Thread]

    def __init__(
        self,
        routing_key: str,
        connection: RpcAsyncConnection,
        query_handler: Callable[[Dict], str],
    ) -> None:
        self.routing_key = routing_key
        self.connection = connection
        self.query_handler = query_handler
        self.closed = False
        self._consuming = False
        self.prefetch_count = 1
        connection.register_client(
            self.routing_key,
            on_channel_open=self.on_channel_open,
            on_connection_close=self.on_connection_close,
        )

    def on_channel_open(self, channel: Channel):
        self.channel = channel
        channel.add_on_close_callback(self.on_channel_close)
        channel.queue_declare(queue=self.routing_key, callback=self.on_queue_declare)

    def on_channel_close(self, channel, reason):
        LOGGER.info(f"closing [{self.routing_key}] for {reason}")
        self.closed = True

    def on_connection_close(self, connection, reason):
        LOGGER.info(f"closing the connection callback, for {reason} reason")

    def on_queue_declare(self, frame: Method):
        LOGGER.info(f"queue declare ok, going to set qos")
        self.channel.basic_qos(
            prefetch_count=self.prefetch_count, callback=self.on_qos_declare
        )

    def on_qos_declare(self, frame: Method):
        LOGGER.info(f"qos declare ok, going to start consuming")
        self.channel.add_on_cancel_callback(self.on_cancel_consume)
        self.consumer_tag = self.channel.basic_consume(
            self.routing_key, on_message_callback=self.on_message_recieve
        )
        self._consuming = True

    def on_cancel_consume(self, frame: Method):
        LOGGER.info("Consumer was cancelled remotely, shutting down: %r", frame)
        self.channel.close()

    def on_message_recieve(
        self, channel: Channel, method, props: BasicProperties, body: bytes
    ):
        """
        Delegate the recieved message to a new thread.
        Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel _unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param bytes body: The message body

        """
        LOGGER.info(
            "Received message # %s from %s",
            method.delivery_tag,
            props.app_id,
        )

        thread = threading.Thread(
            target=self._handle_message, args=(channel, method, props, body)
        )
        thread.start()

    def _handle_message(self, channel, method, props, body):
        """Handle the recieved message"""
        try:
            LOGGER.info(f" [x] Received text: -{body}-"[:LOG_MAX_LENGTH] + "...")
            LOGGER.info(f" [x] recieved correlation_id: [{props.correlation_id}]")
            LOGGER.info(f" [x] recieved routing_key: [{props.reply_to}]")
            response = self.query_handler(json.loads(body))
        except Exception as e:
            traceback.print_exc()
            if channel.is_open:
                channel.basic_nack(delivery_tag=method.delivery_tag)
            else:
                LOGGER.info(f"Channel had been closed")
            return
        try:
            if channel.is_open:
                channel.basic_publish(
                    exchange="",
                    routing_key=props.reply_to,
                    properties=BasicProperties(correlation_id=props.correlation_id),
                    body=response,
                )
                channel.basic_ack(delivery_tag=method.delivery_tag)
                LOGGER.info(" [x] Done")
            else:
                LOGGER.info("Connection had been closed")
        except Exception as e:
            traceback.print_exception(e)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        LOGGER.info("Sending a Basic.Cancel RPC command to RabbitMQ")
        cb = functools.partial(self.on_cancel_declare, userdata=self.consumer_tag)
        self.channel.basic_cancel(self.consumer_tag, cb)

    def on_cancel_declare(self, frame: Method, userdata: str):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method _unused_frame: The Basic.CancelOk frame
        :param str|unicode userdata: Extra user data (consumer tag)

        """
        self._consuming = False
        LOGGER.info(
            "RabbitMQ acknowledged the cancellation of the consumer: %s", userdata
        )
        self.channel.close()
