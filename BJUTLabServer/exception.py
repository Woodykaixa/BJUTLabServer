from werkzeug import exceptions as WerkzeugException


class APIReinitializationError(Exception):
    """
    当已经存在一个API模块的class(inform，etc)实例时，如果尝试创建另一个，则会抛出此异常
    """
    pass


class ParameterException(WerkzeugException.HTTPException):
    """
    用于API的参数异常的情况.

    Note
    ----
    为了错误提示的内容和格式统一，不应当直接抛出此异常。缺少参数时应使用
    :class:`MissingParameter`，参数不合法应使用 :class:`InvalidParameter` 替代。
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
    返回一个 :class:`InvalidParameter`提示API的调用者: 某个参数的格式有误。

    :param param_name: 格式有误的参数的参数名
    :param format_str: 正确的格式(如果是None则不会在提示中附带正确格式信息)
    :return: 一个包含格式错误信息的InvalidParameter对象
    """
    desc = '{} has wrong format'.format(param_name)
    if format_str is not None:
        desc += '({})'.format(format_str)
    return InvalidParameter(400, desc)


def UnsupportedTypeError(type_code: int or str) -> InvalidParameter:
    """
    返回一个 :class:`InvalidParameter`提示API的调用者: 某个参数的类型( `type code `)
    不被API支持。

    :param type_code: 不被支持的类型
    :return: 一个包含类型错误信息的InvalidParameter对象
    """
    # TODO: 返回信息中添加出错的参数名提示
    return InvalidParameter(400, 'unsupported type: {}'.format(type_code))


def DateError(param_name: str, bound: list) -> InvalidParameter:
    """
    返回一个 :class:`InvalidParameter`提示API的调用者: 某个 :class:`date` 类型的参数不符合规定。
    规定API调用的日期与服务端接收到请求时候的日期时间不超过五分钟。

    :param param_name: 日期有误的参数的参数名
    :param bound: 可以被接受的API日期范围(通常是[0,300]，单位：秒)
    :return: 一个包含日期错误信息的InvalidParameter对象
    """
    return InvalidParameter(400, '{} is out of range({} seconds)'.format(param_name, bound))


def RangeError(param_name: str, bound: list) -> InvalidParameter:
    """
    返回一个 :class:`InvalidParameter`提示API的调用者: 某个参数超出了API可接受范围。

    :param param_name: 超出范围的参数的参数名
    :param bound: 可以被API接收的范围
    :return: 一个包含参数超出范围的错误信息的InvalidParameter对象
    """
    return InvalidParameter(400, '{} is out of range({})'.format(param_name, bound))
