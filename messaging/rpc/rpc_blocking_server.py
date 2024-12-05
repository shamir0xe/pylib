import time
import json
import logging
from typing import Callable, Dict
from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from .rpc_blocking_connection import RpcBlockingConnection
from ...config.config import Config

LOGGER = logging.getLogger(__name__)


class RpcBlockingServer:
    routing_key: str
    channel: BlockingChannel
    query_handler: Callable[[Dict], str]

    def __init__(
        self,
        routing_key: str,
        connection: RpcBlockingConnection,
        query_handler: Callable[[Dict], str],
    ) -> None:
        self.routing_key = routing_key
        self.channel = connection.connection.channel()
        self.routing_key = routing_key
        self.query_handler = query_handler
        self.precalc()

    def precalc(self) -> None:
        # fetch one task per worker at a time
        LOGGER.info(f"declaring {self.routing_key} queue")
        self.channel.queue_declare(queue=self.routing_key)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.routing_key, on_message_callback=self.on_query
        )

    def on_query(self, channel, method, props, body):
        LOGGER.info(f" [x] Received text: -{body}-")
        LOGGER.info(f" [x] recieved correlation_id: [{props.correlation_id}]")
        LOGGER.info(f" [x] recieved routing_key: [{props.reply_to}]")
        response = self.query_handler(json.loads(body))

        channel.basic_publish(
            exchange="",
            routing_key=props.reply_to,
            properties=BasicProperties(correlation_id=props.correlation_id),
            body=response,
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)
        LOGGER.info(" [x] Done")

    def start(self) -> None:
        LOGGER.info(" [*] Waiting for messages. To exit press CTRL+C")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            LOGGER.info(f"keyboard interrupt, shutting down...")
            self.channel.close()
        except Exception as e:
            retry_seconds = Config.read("messaging.retry_seconds")
            logging.info(
                f"exception occured: {e}, trying out to create the server \
                again in {retry_seconds}"
            )
            time.sleep(retry_seconds)
            return self.start()
