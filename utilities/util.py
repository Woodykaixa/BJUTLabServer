import exception
import json
from flask import make_response
from werkzeug.datastructures import ImmutableMultiDict


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
    :param e:
    :return:
    """
    res = make_response((
        json.dumps({
            'err': e.description
        }), e.code))
    res.headers['Content-Type'] = 'application/json'
    return res
