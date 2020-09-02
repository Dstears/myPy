import logging
import colorlog

log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}


def get_logger(logger_name):
    console_handler = logging.StreamHandler()

    # 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
    console_handler.setLevel(logging.DEBUG)

    console_formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
        datefmt='%Y-%m-%d  %H:%M:%S',
        log_colors=log_colors_config
    )
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger('logger_name')
    logger.setLevel(logging.DEBUG)
    # 重复日志问题：
    # 1、防止多次addHandler；
    # 2、loggername 保证每次添加的时候不一样；
    # 3、显示完log之后调用removeHandler
    if not logger.handlers:
        logger.addHandler(console_handler)

    console_handler.close()
    return logger
