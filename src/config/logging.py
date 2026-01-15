import logging as logs


def setup_logger(log_level: str, name: str) -> logs.Logger:
    formatter = logs.Formatter(
        fmt="%(asctime)s %(name)s [%(levelname)s] %(message)s - %(module)s:%(filename)s:%(funcName)s:%(lineno)d",
        datefmt="%y.%m.%d %H:%M:%S",
    )

    logger = logs.getLogger(name)
    logger.setLevel(getattr(logs, log_level))

    console_handler = logs.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
