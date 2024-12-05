import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from .rpc_blocking_connection import RpcBlockingConnection
from ...string.generate_id import GenerateId


class RpcBlockingClient(ABC):
    channel: BlockingChannel
    corr_id: str
    future: asyncio.Future
    routing_key: str
    timer: asyncio.Task

    def __init__(self, routing_key: str, connection: RpcBlockingConnection) -> None:
        self.routing_key = routing_key
        self.channel = connection.connection.channel()
        self.init()
        self._precalc()

    @abstractmethod
    def init(self) -> None:
        """This should be implemented in order to set routing_key and..."""

    def _precalc(self) -> None:
        logging.info(f"in the precalc")

        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def on_response(self, ch, method, props, body):
        logging.info(
            f"[{props.correlation_id}]//[{self.corr_id}]: we've receved {body}"
        )
        if self.corr_id == props.correlation_id:
            self.future.set_result(body)

    def _new_correlation_id(self) -> None:
        self.corr_id = GenerateId.generate()

    async def call(self, input: Dict):
        self.future = asyncio.Future()
        self._new_correlation_id()
        self.publish(json.dumps(input))
        logging.info(f"awaiting for the future task")
        return await self.future

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
