from dataclasses import dataclass
import json
import logging
from typing import Dict


from ..rpc.rpc_async_connection import RpcAsyncConnection
from .client_manager import ClientManager


LOGGER = logging.getLogger("[ClientCaller]")


@dataclass
class ClientCaller:
    client_name: str
    rpc_connection: RpcAsyncConnection

    async def call(self, input: Dict):
        LOGGER.info(f"[ClientCaller] adding async rpc client")
        id, client = await ClientManager().get_client(
            client_name=self.client_name,
            rpc_connection=self.rpc_connection,
        )
        res = "{}"
        cycle = True
        while cycle:
            cycle = False
            try:
                res = await client.call(input=input)
            except Exception as e:
                LOGGER.info(f"[ClientCaller] Message Call got error: {e}")
                if str(e).lower().find("connection") >= 0:
                    ClientManager().renew_client(
                        id=id, rpc_connection=self.rpc_connection
                    )
                    cycle = True
        ClientManager().release_client(id=id)
        return json.loads(res)  # type:ignore
