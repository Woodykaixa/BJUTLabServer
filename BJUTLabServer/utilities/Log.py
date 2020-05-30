"""
`Log.py` 提供了 :class:`Log` 用于获取一个配置好的logger。logger是python标注模块自带的
:class:`logging.Logger` 类。
"""
import logging.config


class Log:
    """
    Log使用私有成员对 `get_logger` 返回的logger进行配置，防止意外的配置改动。
    """
    __Config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(levelname)s [%(name)s] <%(asctime)s>: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'filters': {},
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'standard',
                'when': 'H',
                'interval': 24,
                'backupCount': 10,
                'encoding': 'utf-8'
            },
        },
        'loggers': {
            '': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

    @staticmethod
    def get_logger(name, path: str = 'log/BJUTLab.log'):
        """
        获取一个配置好的 `logger`

        :param name: logger的名字
        :param path: 日志文件的存放目录, 使用默认的路径即可。(可以修改日志的目录是个历史遗留问题)
        :return: 用于记录日志的logger
        """
        Log.__Config['handlers']['file']['filename'] = path
        logging.config.dictConfig(Log.__Config)
        return logging.getLogger(name)
