import logging
import functools
import os


def _generate_log(path):
    """
    Create a logger object
    :param path: Path of the log file.
    :return: Logger object.
    """
    # Create a logger and set the level.
    logger = logging.getLogger('LogError')
    logger.setLevel(logging.ERROR)

    # Create file handler, log format and add the format to file handler
    file_handler = logging.FileHandler(path)

    # See https://docs.python.org/3/library/logging.html#logrecord-attributes
    # for log format attributes.
    log_format = '%(levelname)s %(asctime)s %(message)s'
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


PATH = os.path.dirname(os.path.abspath(__file__)) + '/log.error.log'


def log_error(path=PATH):
    """
    We create a parent function to take arguments
    :param path:
    :return:
    """

    def error_log(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            try:
                # Execute the called function, in this case `divide()`.
                # If it throws an error `Exception` will be called.
                # Otherwise it will be execute successfully.
                return func(*args, **kwargs)
            except Exception as e:
                logger = _generate_log(path)
                error_msg = 'And error has occurred at /' + func.__name__ + '\n'
                logger.exception(error_msg)

                return e  # Or whatever message you want.

        return wrapper

    return error_log
