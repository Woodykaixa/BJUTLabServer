import re
from ..exception import FormatError, UnsupportedTypeError, DateError
from typing import Tuple, List
from datetime import datetime, timedelta


class Validator:
    """
    ``Validator``提供了许多静态方法用于验证参数的正确性，只有经过验证的合法参数才能被api调用。
    所有的静态方法均接收一个tuple作为参数，tuple中的第1个元素(index 0)永远是参数的名字,第2个
    元素是参数的值(value)，剩余参数取决于具体调用的静态方法。所有方法返回值都为tuple类型，第
    一个元素是bool类型，表示验证是否通过，第二个类型是exception(如果验证不通过)或None.
    """

    __ValidateResult = (bool, Exception or None)

    school_id_format = r'^G?\d{8}$'

    @staticmethod
    def string_format(param: Tuple[str, str, str]) -> __ValidateResult:
        """
        第三个参数是正则表达式字符串。
        """
        match = re.match(param[2], param[1])
        if match:
            return True, None
        return False, FormatError(param[0], param[2])

    @staticmethod
    def isdigit(param: Tuple[str, str]) -> __ValidateResult:
        if param[1].isdigit():
            return True, None
        return False, FormatError(param[0], 'digit')

    @staticmethod
    def __check_in_range(in_range: bool, exception: Exception) -> __ValidateResult:
        return in_range, None if in_range else exception

    @staticmethod
    def string_length(param: Tuple[str, str, Tuple[int or None,
                                                   int or None]]) -> __ValidateResult:
        """
        第三个参数是一个元组，用于表示``value``长度应处于某一个闭区间。元组的第一个元素是长度下界，
        第二个参数是长度上界,二者都可以是None.
        """
        bound = param[2]
        if bound[0] is None and bound[1] is None:
            return True, None
        length = len(param[1])
        # 其实下面这行把元组转换成列表是为了输出提示的时候更符合直觉，小括号的第一反应是开区间
        fe = FormatError(param[1], 'length:{}'.format(list(bound)))
        if bound[0] is not None and bound[1] is not None:
            in_range = bound[0] <= length <= bound[1]
            return Validator.__check_in_range(in_range, fe)
        if bound[0] is None:
            in_range = length <= bound[1]
            return Validator.__check_in_range(in_range, fe)
        in_range = bound[0] <= length
        return Validator.__check_in_range(in_range, fe)

    @staticmethod
    def acceptable_types(param: Tuple[str, str, List[str or int]]) -> __ValidateResult:
        """
        第三个参数是一个列表，value应当为列表中的某一个值。
        """
        if param[1] in param[2]:
            return True, None
        return False, UnsupportedTypeError(param[1])

    @staticmethod
    def datetime_in_range(param: Tuple[str, str, str, datetime,
                                       Tuple[int or None, int or None]]) -> __ValidateResult:
        """
        第三个参数是日期的格式，第四个参数是参考值，第五个参数是一个元组，日期和参考值的差应当在此
        闭区间内。(单位为秒)
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
                return Validator.__check_in_range(in_range, de)
            if bound[0] is None:
                in_range = delta <= timedelta(seconds=bound[1])
                return Validator.__check_in_range(in_range, de)
            in_range = timedelta(seconds=bound[0]) <= delta
            return Validator.__check_in_range(in_range, de)
        except ValueError:
            return False, FormatError(param[0], param[2])
