import logging

LOGGER = logging.getLogger(__name__)


def spy_logger(func):
    def wrapper(*args, **kwargs):
        LOGGER.info(f"Running: '{func.__name__}', args '{args}', kwargs '{kwargs}'.")
        result = func(*args, **kwargs)
        if result:
            LOGGER.info(f"Result: {result}")
        return result

    return wrapper


def none_logger(func):
    def wrapper(*args, **kwargs):
        LOGGER.exception(f"None object does not have function '{func.__name__}'. Skipped.")
        result = func(*args, **kwargs)
        return result

    return wrapper
