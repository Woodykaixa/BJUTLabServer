import re
from ..exception import (
    FormatError,
    UnsupportedTypeError,
    DateError,
    RangeError
)
from typing import Tuple, List
from datetime import datetime, timedelta


class Validator:
    """
    :class:`Validator` 提供了许多静态方法用于验证参数的正确性，只有经过验证的合法参数才能被api调用。
    所有的静态方法均接收一个 :class:`tuple` 作为参数，参数中的第1个元素(index 0)是参数的名字,第2个
    元素是参数的值(value)，剩余参数取决于具体调用的静态方法。所有方法返回值都为 `tuple` 类型，第
    一个元素是 `bool` 类型，表示验证是否通过，第二个类型是 `exception` (如果验证不通过)或 `None` .
    """

    __ValidateResult = (bool, Exception or None)

    school_id_format = r'^(\d{8}|\d{5})$'

    @staticmethod
    def string_format(param: Tuple[str, str, str]) -> __ValidateResult:
        """
        用于验证 `value` 是否符合某个格式。第三个参数是正则表达式字符串。
        """
        match = re.match(param[2], param[1])
        if match:
            return True, None
        return False, FormatError(param[0], param[2])

    @staticmethod
    def isdigit(param: Tuple[str, str]) -> __ValidateResult:
        """
        验证 `value` 是不是一个数字
        """
        if param[1].isdigit():
            return True, None
        return False, FormatError(param[0], 'digit')

    @staticmethod
    def __check_in_range(val: int, bound: Tuple[int or None, int or None]) -> bool:
        if bound[0] is not None and bound[1] is not None:
            in_range = bound[0] <= val <= bound[1]
        elif bound[0] is None:
            in_range = val <= bound[1]
        else:
            in_range = bound[0] <= val
        return in_range

    @staticmethod
    def __check_in_range_result(in_range: bool, exception: Exception) -> __ValidateResult:
        return in_range, None if in_range else exception

    @staticmethod
    def digit_in_range(param: Tuple[str, int,
                                    Tuple[int or None, int or None]]) -> __ValidateResult:
        """
        验证 `value` 作为 `int` 是否在某个范围内。第三个参数是一个元组，用于表示 `value` 的大小
        应该处于某一个闭区间。元组的第一个元素是 `value` 的下界，如果为 `None` 表示 `value` 的
        值无下限；第二个元素是上界，如果为 `None` 表示无上限。
        """
        bound = param[2]
        if bound[0] is None and bound[1] is None:
            return True, None
        range_e = RangeError(param[0], list(bound))
        in_range = Validator.__check_in_range(param[1], bound)
        return Validator.__check_in_range_result(in_range, range_e)

    @staticmethod
    def string_length(param: Tuple[str, str,
                                   Tuple[int or None, int or None]]) -> __ValidateResult:
        """
        检查 `value` 作为字符串的长度。第三个参数是一个元组，用于表示 `value` 长度应处于某一个闭区间。
        元组的第一个元素是长度下界，如果为 `None` 表示长度无下限；第二个元素是长度上界，如果为 `None`
        表示长度无上限。
        """
        bound = param[2]
        if bound[0] is None and bound[1] is None:
            return True, None
        length = len(param[1])
        # 其实下面这行把元组转换成列表是为了输出提示的时候更符合直觉，小括号的第一反应是开区间
        fe = FormatError(param[1], 'length:{}'.format(list(bound)))
        in_range = Validator.__check_in_range(length, bound)
        return Validator.__check_in_range_result(in_range, fe)

    @staticmethod
    def acceptable_types(param: Tuple[str, str or int, List[str or int]]) -> __ValidateResult:
        """
        检查 `value` 是否是API可接受的类型( `type code` )。第三个参数是一个列表， `value` 应当为
        列表中的某一个值。列表或 `value` 可以是 `int` 或 `str` ，如果 `value` 不在列表中，则会把
        `value` 和列表都转换成 `str` 类型再次检索，两次检索均不存在才会返回 `False`。
        """
        val = param[1]
        if val in param[2]:
            return True, None
        if type(val) is not str:
            val = str(val)
            if val in param[2]:
                return True, None
        else:
            types = [str(t) for t in param[2] if type(t) is not str]
            if val in types:
                return True, None
        return False, UnsupportedTypeError(param[1])

    @staticmethod
    def datetime_in_range(param: Tuple[str, str, str, datetime,
                                       Tuple[int or None, int or None]]) -> __ValidateResult:
        """
        检查 `value` 作为 :class:`datetime` 是否在给定的区间内。第三个参数是日期的格式(type= `str` )，
        第四个参数是参考值(type= `datetime` )，第五个参数是一个元组，日期和参考值的差应当在此闭区间内。
        (单位为秒)，区间的上界和下界以及判定于 `Validator.digit_in_range()` 相同。

        """
        try:
            dt = datetime.strptime(param[1], param[2])
            bound = param[4]
            if bound[0] is None and bound[1] is None:
                return True, None
            delta = dt - param[3]
            de = DateError(param[0], list(bound))
            if bound[0] is not None and bound[1] is not None:
                in_range = timedelta(seconds=bound[0]) <= delta <= timedelta(seconds=bound[1])
                return Validator.__check_in_range_result(in_range, de)
            if bound[0] is None:
                in_range = delta <= timedelta(seconds=bound[1])
                return Validator.__check_in_range_result(in_range, de)
            in_range = timedelta(seconds=bound[0]) <= delta
            return Validator.__check_in_range_result(in_range, de)
        except ValueError:
            return False, FormatError(param[0], param[2])
