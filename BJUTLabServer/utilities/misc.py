import json
from functools import wraps

from flask import make_response, session
from werkzeug.datastructures import ImmutableMultiDict

from .. import exception


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


def get_form_data_by_key(form: ImmutableMultiDict, key: str):
    """
    根据key，从表单中获取对应value，如果key不存在则会抛出一个
    :param form: http请求的表单参数
    :param key: 表单中的一个key
    :return: ``key``对应的value, 即``form[key]``
    """
    try:
        return form[key]
    except KeyError:
        raise exception.ParameterException(400, 'Missing parameter: {}'.format(key))


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
                and 'school_id' in session \
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