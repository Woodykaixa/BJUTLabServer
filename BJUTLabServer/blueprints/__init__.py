"""
blueprints模块负责提供API的视图函数，视图函数负责验证请求参数的正确性，只有参数准确无误才会调用
api模块中对应的业务逻辑处理函数并返回其调用结果，否则会返回 :class:`BJUTLabServer.exception.ParameterException`
的子类来提示调用者调用API出错。
"""
from .Inform import InformBP
from .Auth import AuthBP
from .Experiment import ExpBP

BPList = [InformBP, AuthBP, ExpBP]
