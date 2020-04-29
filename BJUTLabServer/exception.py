from werkzeug import exceptions as WerkzeugException


class APIReinitializationError(Exception):
    """
    当已经存在一个api模块的class(inform，etc)实例时，如果尝试创建另一个，则会抛出此异常
    """
    pass


class ParameterException(WerkzeugException.HTTPException):
    """
    当调用api时提供的参数与api的参数不同时，则抛出此异常。
    DEPRECATED!! - 为了返回信息的统一，不推荐使用此异常。缺少参数时应使用``MissingParameter``,
    参数不合法应使用``InvalidParameter``替代
    """

    def __init__(self, code, desc):
        ParameterException.code = code
        ParameterException.description = desc


class InvalidParameter(ParameterException):
    """
    当调用API时参数不符合规定时，抛出此异常。
    """

    def __init__(self, code, desc):
        InvalidParameter.code = code
        InvalidParameter.description = 'Invalid parameter: {}'.format(desc)


class MissingParameter(ParameterException):
    """
    当调用API缺少参数时抛出此异常。
    """

    def __init__(self, code, desc):
        MissingParameter.code = code
        MissingParameter.description = 'Missing parameter: {}'.format(desc)


def FormatError(param_name: str) -> InvalidParameter:
    """
    这是一个看起来像异常类的函数，你完全可以按照抛出异常的方式使用它。
    `
        raise FormatError('id')
    `
    """
    return InvalidParameter(400, '{} has wrong format'.format(param_name))


def UnsupportedTypeError(type_code: int) -> InvalidParameter:
    return InvalidParameter(400, 'unsupported type: {}'.format(type_code))
