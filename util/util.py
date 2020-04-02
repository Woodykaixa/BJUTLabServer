def none_check(code: int, msg: str, *args):
    for param in args:
        if param is None:
            return {
                'hasNone': True,
                'msg': {
                    'code': code,
                    'err': msg.format(args.index(param))
                }}
    return {
        'hasNone': False
    }
