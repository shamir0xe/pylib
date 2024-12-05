import functools
import logging
from ..messaging.rpc.rpc_blocking_connection import RpcBlockingConnection

LOGGER = logging.getLogger(__name__)


def inject_blocking_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = RpcBlockingConnection()
            kwargs["blocking_connection"] = connection
            result = func(*args, **kwargs)
            connection.close()
            return result
        except Exception as e:
            LOGGER.info(f"exception occured {e}")
            if connection:
                connection.close()

    return wrapper
