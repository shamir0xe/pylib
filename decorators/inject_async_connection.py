import functools
import traceback
import logging
from ..config.config import Config
from ..messaging.rpc.rpc_async_connection import RpcAsyncConnection

LOGGER = logging.getLogger(__name__)


def inject_async_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = RpcAsyncConnection(url=Config.read_env("message_broker.url"))
            kwargs["async_connection"] = connection
            result = func(*args, **kwargs)
            if connection and connection.inner_connection:
                connection.inner_connection.stop()
            return result
        except Exception as e:
            traceback.print_exc()
            LOGGER.info(f"exception occured in inject wrapper: {e}")
            if connection and connection.inner_connection:
                connection.inner_connection.stop()
        finally:
            LOGGER.info("[inject-async-connection] Closure")

    return wrapper
