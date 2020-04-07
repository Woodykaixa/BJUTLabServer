from werkzeug import exceptions as WerkzeugException


class APIReinitializationError(Exception):
    """
    当已经存在一个api模块的class(inform，etc)实例时，如果尝试创建另一个，则会抛出此异常
    """
    pass


class ParameterException(WerkzeugException.HTTPException):
    """
    当调用api时提供的参数与api的参数不同时，则抛出此异常
    """
    def __init__(self, code, desc):
        ParameterException.code = code
        ParameterException.description = desc
