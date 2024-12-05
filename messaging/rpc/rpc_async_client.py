import asyncio
import json
import logging
from typing import Dict
from pika import BasicProperties
from pika.channel import Channel
from pika.frame import Method
from .rpc_async_connection import RpcAsyncConnection
from ...string.generate_id import GenerateId
from ...asynchrone.get_or_create_event_loop import GetOrCreateEventLoop

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)
LOG_MAX_LENGTH = 222


class RpcAsyncClient:
    channel: Channel
    routing_key: str
    closed: bool = False
    ready: bool = False
    future: asyncio.Future

    def __init__(
        self,
        routing_key: str,
        connection: RpcAsyncConnection,
    ) -> None:
        self._deliveries = {}
        self._acked = 0
        self._nacked = 0
        self._message_number = 0
        self.routing_key = routing_key
        connection.register_client(
            self.routing_key,
            on_channel_open=self.on_channel_open,
            on_connection_close=self.on_connection_close,
        )

    def on_channel_open(self, channel: Channel):
        LOGGER.info(f"channel oppened")
        self.channel = channel
        channel.add_on_close_callback(self.on_channel_close)
        channel.queue_declare(queue="", exclusive=True, callback=self.on_queue_declare)
        channel.confirm_delivery(self.on_delivery_confirmation)

    def on_channel_close(self, channel, reason):
        LOGGER.info(f"closing [{self.routing_key}] for {reason}")
        self.closed = True

    def on_connection_close(self, connection, reason):
        LOGGER.info(f"closing connection")
        pass

    def on_queue_declare(self, frame: Method):
        LOGGER.info(f"queue declared ok")
        self.callback_queue = frame.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )
        self.ready = True

    def on_response(self, ch, method, props, body):
        logging.info(
            f"[{props.correlation_id}]//[{self.corr_id}]: we've receved {body}"[
                :LOG_MAX_LENGTH
            ]
        )
        if self.corr_id == props.correlation_id:
            logging.info(f"releasing {props.correlation_id}")
            err_count = 0
            try:
                GetOrCreateEventLoop().event_loop.run_in_executor(
                    None, self.future.set_result, body
                )
            except Exception as _:
                err_count += 1
                # LOGGER.info(f"exception on_response: {e}")
                # traceback.print_exc()
            # try:
            #     self.future.set_result(body)
            # except Exception as _:
            #     err_count += 1
            #     # LOGGER.info(f"exception on_response: {e}")
            #     # traceback.print_exc()
            if err_count > 1:
                raise Exception("Cannot set_result for the future")

    def _new_correlation_id(self) -> None:
        self.corr_id = GenerateId.generate()

    async def call(self, input: Dict):
        if not self.ready:
            LOGGER.info(
                f"[Client-Call] channel is not ready yet, retrying in 2.0 seconds"
            )
            await asyncio.sleep(2.0)
            return await self.call(input)
        LOGGER.info(f"[Client-Call] creating self.future")
        self.future = asyncio.Future()
        self._new_correlation_id()
        self.publish(json.dumps(input))
        LOGGER.info(f"[Client-Call] awaiting for the future task")
        await self.future
        LOGGER.info(f"[Client-Call] AFTER WAIT")
        if self.future.exception():
            # Handle the raisen error
            return self.future.exception()
        if self.future.done():
            return self.future.result()
        return None

    async def close(self):
        LOGGER.info("going to close the channel")
        self.channel.close()

    def publish(self, data: str):
        logging.info(f"publishing with corr_id=[{self.corr_id}]")
        self.channel.basic_publish(
            exchange="",
            routing_key=self.routing_key,
            body=data,
            properties=BasicProperties(
                reply_to=self.callback_queue, correlation_id=self.corr_id
            ),
        )
        self._message_number += 1
        self._deliveries[self._message_number] = True
        LOGGER.info("Published message # %i", self._message_number)

    def on_delivery_confirmation(self, method_frame):
        """Invoked by pika when RabbitMQ responds to a Basic.Publish RPC
        command, passing in either a Basic.Ack or Basic.Nack frame with
        the delivery tag of the message that was published. The delivery tag
        is an integer counter indicating the message number that was sent
        on the channel via Basic.Publish. Here we're just doing house keeping
        to keep track of stats and remove message numbers that we expect
        a delivery confirmation of from the list used to keep track of messages
        that are pending confirmation.

        :param pika.frame.Method method_frame: Basic.Ack or Basic.Nack frame

        """
        confirmation_type = method_frame.method.NAME.split(".")[1].lower()
        ack_multiple = method_frame.method.multiple
        delivery_tag = method_frame.method.delivery_tag

        LOGGER.info(
            "Received %s for delivery tag: %i (multiple: %s)",
            confirmation_type,
            delivery_tag,
            ack_multiple,
        )

        if confirmation_type == "ack":
            self._acked += 1
        elif confirmation_type == "nack":
            self._nacked += 1

        if delivery_tag in self._deliveries:
            del self._deliveries[delivery_tag]

        if ack_multiple:
            for tmp_tag in list(self._deliveries.keys()):
                if tmp_tag <= delivery_tag and tmp_tag in self._deliveries:
                    self._acked += 1
                    del self._deliveries[tmp_tag]
        """
        NOTE: at some point you would check self._deliveries for stale
        entries and decide to attempt re-delivery
        """

        LOGGER.info(
            "Published %i messages, %i have yet to be confirmed, "
            "%i were acked and %i were nacked",
            self._message_number,
            len(self._deliveries),
            self._acked,
            self._nacked,
        )
