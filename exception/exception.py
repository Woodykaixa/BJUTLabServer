class APIReinitializationError(Exception):
    """
    当已经存在一个api模块的class(inform，etc)实例时，如果尝试创建另一个，则会抛出此异常
    """
    pass
