"""
`misc.py` 提供了一些函数用于简化开发，使开发者可以专注于业务逻辑而不是复杂重复的流程。
"""
import json
import typing
from datetime import date
from functools import wraps

from flask import make_response, session
from werkzeug.datastructures import ImmutableMultiDict, MultiDict

from .. import exception

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def __validate_param(key, value, validator: typing.Callable, v_param: tuple, nullable: bool):
    """
    参数验证函数，用于验证 `value` 是否符合 `validator` 定义的规则。只有通过验证的参数会被返回。
    参数不合法则会直接抛出异常。
    :param key: 参数名
    :param value: 参数值
    :param validator: 参数验证函数。接收的参数为tuple(``key``,``value``,``v_param``)。如果为None
                      则认为参数合法
    :param v_param: 验证函数使用的额外参数
    :param nullable: 参数是否可以为None，如果为True会直接返回None
    :return: value或None(如果nullable=True)
    """
    if value is None:
        if nullable:
            return value
        raise exception.MissingParameter(400, key)
    if validator is None:
        return value
    validator_param = (key, value,) + v_param if v_param else (key, value,)
    valid, e = validator(validator_param)
    if valid:
        return value
    raise e


def get_validate_param(args: MultiDict, key: str, t: typing.Callable = None,
                       validator: typing.Callable = None, v_param: tuple = None,
                       nullable: bool = False):
    """
    为GET API检查参数编写。从 `args` 中获取参数，使用 `utilities.misc.__validate_param` 验证是否合法。
    只有合法的参数会被返回。不合法的参数会抛出异常。

    :param args: 存放参数的字典
    :param key: 参数名
    :param t: 参数类型转换函数
    :param validator: 参数验证函数
    :param v_param: 传给validator的额外参数
    :param nullable: 参数是否可以为None，如果为True会直接返回None
    :return: 等同于flask的args.get(key, default=None, type=t)
    """
    value = args.get(key, None, t)
    return __validate_param(key, value, validator, v_param, nullable)


def post_validate_param(form: ImmutableMultiDict, key: str,
                        validator: typing.Callable = None, v_param: tuple = None,
                        nullable: bool = False) -> str or None:
    """
    为POST API检查参数编写。从 `form` 中获取参数，使用 `utilities.misc.__validate_param` 验证是否合法。
    只有合法的参数会被返回。不合法的参数会抛出异常。

    :param form: 存放参数的字典
    :param key: 参数名
    :param validator: 参数验证函数
    :param v_param: 传给validator的额外参数
    :param nullable: 参数是否可以为None，如果为True会直接返回None
    :return: 等同于form[key]
    """
    value = form[key] if key in form else None
    return __validate_param(key, value, validator, v_param, nullable)


def make_error_response(e: exception.WerkzeugException.HTTPException):
    """
    当发生错误时，产生响应数据，发送 :class:`werkzeug.exceptions.HTTPException` `e` 的信息(JSON格式)
    :return: 返回状态码为 `e.code` 的错误响应

    Note
    ----
    为了使API返回错误的形式和API正确调用返回结果的形式相同，使用本函数覆盖原有的错误响应逻辑，返回JSON格
    式信息。
    """
    res = make_response((
        json.dumps({
            'err': e.description
        }), e.code))
    res.headers['Content-Type'] = 'application/json'
    return res


def login_required(view):
    """
    这个函数通常以装饰器的形式使用，用于限定被装饰的视图函数只能在用户登录后调用。
    如果用户未登录会抛出 :class:`exception.WerkzeugException.Unauthorized`

    :param view: 被装饰的视图函数
    :type view: function
    :return: 如果用户已登录，则返回视图函数
    """

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'name' in session \
                and 'id' in session \
                and 'password' in session \
                and 'type' in session:
            return view(*args, **kwargs)
        unauthorized_exception = exception.WerkzeugException.Unauthorized
        unauthorized_exception.description = 'Login Required'
        raise unauthorized_exception

    return wrapped_view


def jsonify(obj: object):
    """
    对 `json.dumps` 的简单封装，防止每次都忘记加上 `ensure_ascii=False`
    :param obj: 将被序列化的对象
    :return: 序列化后的字符串
    """
    return json.dumps(obj, ensure_ascii=False)


def parse_date_str(param_name: str, date_str: str) -> date:
    """
    将 `date_str` 转换为 :class:`date` 类型

    :param param_name: API参数的名字，转换 `date_str` 失败时抛出的异常用这个参数名给用户提示。
    :param date_str: 字符串形式的日期
    :return: 返回转换后的date对象
    """
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        raise exception.FormatError(param_name)
