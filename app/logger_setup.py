import logging


def get_logger(name: str = __name__):
    """Return a configured logger with level INFO.

    This uses a stream handler and simple timestamped formatter. If the
    logger already has handlers it will not re-add them (safe to call
    multiple times).
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
