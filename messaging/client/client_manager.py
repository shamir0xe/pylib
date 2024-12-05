import logging
from typing import Dict, List, Tuple

from ...database.session_pools import singleton
from ...decorators.thread_lock import thread_lock
from ...messaging.rpc.rpc_async_client import RpcAsyncClient
from ...messaging.rpc.rpc_async_connection import RpcAsyncConnection

LOGGER = logging.getLogger(__name__)


@singleton
class ClientManager:
    clients: List[Tuple[str, bool]]
    mapper: Dict[int, RpcAsyncClient]

    def __init__(self) -> None:
        LOGGER.info("[ClientManager] CLIENT MANAGER have been initialized")
        self.clients = []
        self.mapper = {}

    def renew_client(self, id: int, rpc_connection: RpcAsyncConnection) -> None:
        LOGGER.info(f"[ClientManager] Renew the client")
        self.mapper[id] = RpcAsyncClient(
            routing_key=self.clients[id][0],
            connection=rpc_connection,
        )

    def new_client(self, client_name: str, rpc_connection: RpcAsyncConnection):
        LOGGER.info(f"[ClientManager] Creating new client for {client_name}")
        self.clients += [(client_name, False)]
        id = len(self.clients) - 1
        self.mapper[id] = RpcAsyncClient(
            routing_key=client_name,
            connection=rpc_connection,
        )

    @thread_lock
    async def get_client(
        self, client_name: str, rpc_connection: RpcAsyncConnection
    ) -> Tuple[int, RpcAsyncClient]:
        LOGGER.info(f"[ClientManager] GETTING CLIENT for {client_name}")
        for id, (cl_name, available) in enumerate(self.clients):
            if available and cl_name == client_name:
                self.clients[id] = client_name, False
                return id, self.mapper[id]
        self.new_client(client_name, rpc_connection)
        id = len(self.clients) - 1
        return id, self.mapper[id]

    def release_client(self, id: int):
        self.clients[id] = self.clients[id][0], True

    async def cleanup(self) -> None:
        LOGGER.info("[ClientManager] Cleanup")
        ## TODO: await the process
        for id, client in self.mapper.items():
            LOGGER.info(f"[#{id}] goint to be closed")
            await client.close()
