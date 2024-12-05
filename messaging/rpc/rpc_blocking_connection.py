import logging
from pika import BlockingConnection, ConnectionParameters
from ...decorators.singleton import singleton
from ...config.config import Config


@singleton
class RpcBlockingConnection:
    conncetion: BlockingConnection

    def __init__(self) -> None:
        self.connection = BlockingConnection(
            ConnectionParameters(host=Config.read_env("message_broker.host"))
        )

    def close(self):
        logging.info(f"cleaning the timer")
        self.connection.close()
