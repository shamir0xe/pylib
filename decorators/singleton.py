import functools


def singleton(cls):
    """Turns class into singleton"""

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if wrapper.instance:  # type: ignore
            return wrapper.instance  # type: ignore
        wrapper.instance = cls(*args, **kwargs)  # type: ignore
        return wrapper.instance  # type: ignore

    wrapper.instance = None  # type: ignore
    return wrapper
