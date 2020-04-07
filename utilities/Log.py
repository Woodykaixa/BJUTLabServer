import logging.config


class Log:
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
        Log.__Config['handlers']['file']['filename'] = path
        logging.config.dictConfig(Log.__Config)
        return logging.getLogger(name)
