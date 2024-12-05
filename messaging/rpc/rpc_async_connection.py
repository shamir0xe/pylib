import asyncio
from concurrent.futures import ThreadPoolExecutor, Future
import logging
import traceback

from pika.channel import Channel
from pika import URLParameters, SelectConnection
from typing import Callable, List, Optional, Tuple
from ...decorators.singleton import singleton
from ...types.exception_types import ExceptionTypes
from ...asynchrone.get_or_create_event_loop import GetOrCreateEventLoop


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)


class InnerRpcAsyncConnection:
    connection: SelectConnection

    def __init__(
        self,
        url: str,
        running_loop_callback: Callable = lambda _: True,
        error_future: Optional[asyncio.Future] = None,
    ) -> None:
        self._url = url
        self.running_loop_handler = running_loop_callback
        self.error_handler_future = error_future
        self._stopping = False
        self._conn_opened = False
        self.should_reconnect = False
        self._on_channel_open: List[Tuple[str, Callable]] = []
        self._on_conn_open_error: List[Tuple[str, Callable]] = []
        self._on_conn_close: List[Tuple[str, Callable]] = []
        self._channels: List[Channel] = []

    def connect(self) -> None:
        LOGGER.info(f"[ASYNC CONNECTION] connecting to message_broker [{self._url}]")
        self.connection = SelectConnection(
            parameters=URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
        )
        self.start()

    def start(self) -> None:
        """Run the RabbitMQ IOLoop in an executor (background thread)."""
        try:
            GetOrCreateEventLoop().event_loop.run_in_executor(
                None, self.connection.ioloop.start
            )
        except Exception:
            traceback.print_exc()

        LOGGER.info("[START] Reached the end")

    def register_client(
        self, client_id: str, on_channel_open: Callable, on_connection_close: Callable
    ):
        """Register client with provided callbacks"""
        self._on_channel_open += [(client_id, on_channel_open)]
        self._on_conn_close += [(client_id, on_connection_close)]
        if self._conn_opened:
            ## Register the channel if the conn has been openned
            self._channels += [
                self.connection.channel(on_open_callback=on_channel_open)
            ]

    def remove_client(self, client_id: str) -> None:
        """Remove the client and it's callbacks"""
        LOGGER.info(f"removing client #{client_id}")
        self._on_channel_open = list(
            filter(lambda tup: tup[0] != client_id, self._on_channel_open)
        )
        self._on_conn_close = list(
            filter(lambda tup: tup[0] != client_id, self._on_conn_close)
        )

    def on_connection_open(self, _connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :param pika.SelectConnection _unused_connection: The connection

        """
        LOGGER.info("Connection opened")
        self._conn_opened = True
        for client_id, callable in self._on_channel_open:
            LOGGER.info(f"[{client_id}]: creating new channel")
            self._channels += [self.connection.channel(on_open_callback=callable)]

    def on_connection_open_error(self, _unused_connection, err):
        """This method is called by pika if the connection to RabbitMQ
        can't be established.

        :param pika.SelectConnection _unused_connection: The connection
        :param Exception err: The error

        """
        LOGGER.error("Connection open failed, reopening in 5 seconds: %s", err)
        self.should_reconnect = True
        # self._run_loop_future.set_exception(Exception("open error"))
        self.stop()

    def on_connection_closed(self, connection, reason):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param Exception reason: exception representing reason for loss of
            connection.

        """
        for client_id, callable in self._on_conn_close:
            LOGGER.info(f"[{client_id}]: close conn callback")
            callable(connection, reason)
        if self._stopping:
            # Already stopping...
            try:
                GetOrCreateEventLoop().event_loop.call_soon_threadsafe(
                    self.connection.ioloop.stop
                )
            except Exception as e:
                LOGGER.warning(f"Cannot close the connection due to {e}")
            # self.connection.ioloop.stop()
        else:
            LOGGER.warning("Connection closed, reopening in 5 seconds: %s", reason)
            self.sould_reconnect = True
            self.stop()

    def close(self) -> None:
        try:
            for channel in self._channels:
                if channel.is_open:
                    channel.close()
            if self.connection.is_open:
                self.connection.close()
        except Exception:
            traceback.print_exc()

    def stop(self):
        LOGGER.info("[STOP]")
        # Close the channels first
        self.close()
        try:
            self.connection.ioloop.stop()
        except Exception as e:
            LOGGER.warning(f"what happened? {e}")

        if not self._stopping:
            self._stopping = True
            LOGGER.info("Stopping")
            for client_id, callable in self._on_conn_close:
                LOGGER.info(f"[{client_id}]: close conn callback")
                callable(self.connection, "smt")
            ## TODO:
            self.should_reconnect = True
            # self.error_handler("disconnected")
            if self.error_handler_future:
                LOGGER.info("HERE")
                try:
                    self.error_handler_future.set_result("disconnected")
                except Exception as e:
                    LOGGER.warning(f"exception occured : {e}")
        else:
            # Already Stopping
            LOGGER.info("[STOP] calling the ioloop.stop")

            # self.connection.ioloop.stop()
        LOGGER.info("Stopped")


@singleton
class RpcAsyncConnection:
    url: str
    rpc_connection: Optional[InnerRpcAsyncConnection]
    client_queue: List[Tuple]

    def __init__(self, url: str) -> None:
        self.url = url
        self.client_queue = []
        self.rpc_connection = None
        self.executor = ThreadPoolExecutor(max_workers=1)
        self._create_connection()

    def _create_connection(self) -> None:
        LOGGER.info("Creating a new connection")
        self._error_future = asyncio.Future()

        # Submit _maybe_reconnect to run asynchronously in the event loop
        future = asyncio.run_coroutine_threadsafe(
            self._maybe_reconnect(), GetOrCreateEventLoop().event_loop
        )
        future.add_done_callback(self._running_loop_handler)

        LOGGER.info("Creating inner RPC async connection")

        if self.rpc_connection:
            del self.rpc_connection

        self.rpc_connection = InnerRpcAsyncConnection(
            url=self.url,
            running_loop_callback=self._running_loop_handler,
            error_future=self._error_future,
        )
        for client_id, on_channel_open, on_connection_close in self.client_queue:
            self.rpc_connection.register_client(
                client_id, on_channel_open, on_connection_close
            )
        self.rpc_connection.connect()

    def _running_loop_handler(self, future: Future):
        """Handle the completion of the future."""
        LOGGER.info(f"[RUNNING LOOP] Future: {future}")
        try:
            result = future.result()  # Handle the result or exception
            LOGGER.info(f"[RUNNING LOOP] Result: {result}")
        except Exception as exc:
            LOGGER.error(f"[RUNNING LOOP] Exception: {exc}")

        LOGGER.info("[RUNNING LOOP] Future finished")

    async def _maybe_reconnect(self) -> None:
        LOGGER.info("[MAYBE-RECONNECT] Waiting for future to respond")
        try:
            LOGGER.info("[MAYBE-RECONNECT] Wait for the future")
            result = await self._error_future  # Wait for the error to happen
            LOGGER.info(f"[MAYBE-RECONNECT] Future responded: {result}")
        except asyncio.CancelledError:
            LOGGER.info("[MAYBE-RECONNECT] Future was cancelled")
            return

        LOGGER.info("[MAYBE-RECONNECT] Checking reconnect condition")
        if self.rpc_connection and self.rpc_connection.should_reconnect:
            LOGGER.info("Reconnecting in 5s...")
            await asyncio.sleep(5)
            self._create_connection()

    @property
    def inner_connection(self) -> InnerRpcAsyncConnection:
        if not self.rpc_connection:
            raise Exception(ExceptionTypes.CONNECTION_INVALID)
        return self.rpc_connection

    def register_client(
        self, client_id: str, on_channel_open: Callable, on_connection_close: Callable
    ):
        if not self.rpc_connection:
            raise Exception(ExceptionTypes.CONNECTION_INVALID)
        self.client_queue += [(client_id, on_channel_open, on_connection_close)]
        return self.rpc_connection.register_client(
            client_id=client_id,
            on_channel_open=on_channel_open,
            on_connection_close=on_connection_close,
        )
