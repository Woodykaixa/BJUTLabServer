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


def FormatError(param_name: str, format_str: str = None) -> InvalidParameter:
    """
    这是一个看起来像异常类的函数，你完全可以按照抛出异常的方式使用它。
    `
        raise FormatError('id')
    `
    """
    desc = '{} has wrong format'.format(param_name)
    if format_str is not None:
        desc += '({})'.format(format_str)
    return InvalidParameter(400, desc)


def UnsupportedTypeError(type_code: int or str) -> InvalidParameter:
    return InvalidParameter(400, 'unsupported type: {}'.format(type_code))


def DateError(param_name: str, bound: list) -> InvalidParameter:
    return InvalidParameter(400, '{} is out of range({} seconds)'.format(param_name, bound))
