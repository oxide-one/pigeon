import logging
import colorlog


def create_logger(verbosity: int = 1) -> logging.Logger:
    """
    Creates a logging instance using colorlog and logger
    :param verbosity: The verbosity level to log at, defaults to 1
    :type varbosity: int, optional
    ...
    :return: A logging instance `logging.logger`
    :rtype: `logging.logger`
    """
    if verbosity >= 3:
        verbosity_level = "DEBUG"
    elif verbosity == 2:
        verbosity_level = "INFO"
    elif verbosity == 1:
        verbosity_level = "WARNING"
    elif verbosity == 0:
        verbosity_level = "ERROR"

    # Grab the attribute for the logging level
    logging_level = getattr(logging, verbosity_level)

    # Set the logging format
    logging_format = "[{asctime:s}] | {log_color:s}{levelname:8s}{reset:s}| {log_color:s}{message:s}{reset:s}"
    handler = logging.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        logging_format,
        reset=True,
        datefmt='%H:%M:%S',
        style='{',
        log_colors={
            'DEBUG':    '',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
        ))
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging_level)
    return logger
