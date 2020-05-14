import json
import typing
from datetime import datetime, timedelta, date
from functools import wraps

from flask import make_response, session
from werkzeug.datastructures import ImmutableMultiDict

from .. import exception

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def none_check(code: int, msg: str, *args):
    """
    检查``*args``中是否存在``None``，如果存在，则抛出``ParameterException``，并且把
    http响应状态码设置为``code``

    :param code: 当存在``None``参数时，http响应的状态码
    :param msg: 当存在``None``参数时，http响应返回的信息
    :param args: 等待检查的参数
    :return:
    """
    for param in args:
        if param is None:
            return {
                'hasNone': True,
                'exception': exception.ParameterException(code, msg.format(args.index(param)))
            }
    return {
        'hasNone': False
    }


def get_and_validate_param(form: ImmutableMultiDict, key: str,
                           validator: typing.Callable = None, v_param: tuple = None,
                           nullable: bool = False) -> str or None:
    """
    从``form``中获取参数，并验证参数是否合法。只有合法的参数会被返回。不合法的参数会抛出异常。
    :param form: 存放参数的字典
    :param key: 待获取参数的键
    :param validator: 验证参数是否合法的函数，参数为``key``,``value``,``v_param``。如果为None
                      则认为参数合法
    :param v_param: 传给``validator``的额外参数，可以为None，
    :param nullable: ``value``可以为None，此时会直接返回None.
    :return:
    """
    value = form[key] if key in form else None
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


def make_error_response(e: exception.WerkzeugException.HTTPException):
    """
    当发生错误时，产生响应数据，发送``HTPPException``的信息
    :return: 返回状态码为``e.code``的错误响应
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
    :param view: 被装饰的视图函数
    :type view: function
    :return: 如果用户已登录，则返回视图函数
    :except: 如果用户未登录会抛出``Unauthorized``
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
    对``json.dumps``的简单封装，防止每次都忘记加上``ensure_ascii=False``
    :param obj: 将被序列化的对象
    :return: 序列化后的字符串
    """
    return json.dumps(obj, ensure_ascii=False)


def parse_date_str(param_name: str, date_str: str) -> date:
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        raise exception.FormatError(param_name)
