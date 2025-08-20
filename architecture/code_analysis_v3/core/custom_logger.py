import logging
import colorlog

LOGGER = logging.getLogger(__name__)


# handler = colorlog.StreamHandler()
# formatter = colorlog.ColoredFormatter(
#     "%(asctime)s %(log_color)s %(levelname)s %(message)s",
#     log_colors={
#         "DEBUG": "cyan",
#         "INFO": "green",
#         "WARNING": "yellow",
#         "ERROR": "red",
#         "CRITICAL": "bold_red",
#     },
#     datefmt="%Y-%m-%d %H:%M:%S",
# )
# handler.setFormatter(formatter)

# logger = logging.getLogger(__name__)
# logger.addHandler(handler)
# # Change the log level to make the logger more verbose
# logger.setLevel(logging.INFO)

DEBUG = True


def spy_logger(func):
    def wrapper(*args, **kwargs):
        if DEBUG:
            LOGGER.info(f"FUNCTION: '{func.__name__}', ARGS '{args}', KWARGS '{kwargs}'.")
            result = func(*args, **kwargs)
            if result is not None:
                LOGGER.info(f"  RESULT: '{func.__name__}' {result}")
            return result
        result = func(*args, **kwargs)

    return wrapper


def none_logger(func):
    def wrapper(*args, **kwargs):
        if DEBUG:
            LOGGER.error(f"None object does not have function '{func.__name__}'. Skipped.")
            result = func(*args, **kwargs)
            return result
        result = func(*args, **kwargs)

    return wrapper
