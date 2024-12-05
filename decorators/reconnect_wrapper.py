import functools
import logging


def reconnect_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if len(args) > 0:
                self = args[0]
                logging.info(
                    f"error occured: {e}\
                trying to reconnect"
                )
                self.connect()
                return func(*args, **kwargs)

    return wrapper
