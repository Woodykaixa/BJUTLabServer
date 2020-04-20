"""
blueprints模块负责提供API的视图函数，视图函数负责验证请求参数的正确性，只有参数准确无误才会调用
api模块的函数并返回API的调用结果
"""
from .Inform import InformBP
from .Auth import AuthBP
