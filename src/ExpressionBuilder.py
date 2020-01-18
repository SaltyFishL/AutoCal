import random
from src.Const import Const


class ExpressionBuilder:
    def __init__(self):
        self.exp_elements_infix = []

    @staticmethod
    def __rand_op_num():
        return random.randint(1, 10)

    @staticmethod
    def __rand_op(mode):
        """mode为Easy时, 整数加减乘除; mode为Medium时, 加分数; mode为Hard时, 加乘方"""
        if mode == Const.Easy or mode == Const.Medium:
            return random.randint(Const.Plus, Const.Div)
        if mode == Const.Hard:
            return random.randint(Const.Plus, Const.Pow)

    @staticmethod
    def __rand_num():
        return random.randint(0, 100)

    @staticmethod
    def __rand_pow_num():
        return random.randint(1, 3)

    def build(self, mode):
        """
        为了便于生成表达式, 也为了方便计算, 做出以下规定:
        1. 一个表达式中最多只有一个乘方运算
        2. 除号和幂运算后不生成左括号
        3. 乘方幂的范围为1, 2, 3
        :param mode:
        :return:
        """
        op_num = ExpressionBuilder.__rand_op_num()
        length = 0
        left_bracket_num = 0
        last_left_bracket = 0
        have_pow = False
        j = 1
        while j <= op_num + 1:
            # 生成一个随机数
            self.exp_elements_infix.append(self.__rand_num())
            length += 1
            # 生成随机数后的处理
            if length > 1 and self.exp_elements_infix[length - 2] == Const.Pow:
                # 乘方运算只能是1, 2, 3
                self.exp_elements_infix[length - 1] = self.__rand_pow_num()
            if length > 1 and self.exp_elements_infix[length - 2] == Const.Div and self.exp_elements_infix[length - 1] == 0:
                # 防止除数为0
                self.exp_elements_infix[length - 1] = 1
            if left_bracket_num > 0 and random.randint(0, 2) == 0 and last_left_bracket > 2:
                # 1/3的概率可以添加右括号
                self.exp_elements_infix.append(Const.RightBracket)
                length += 1
                left_bracket_num -= 1
                last_left_bracket = 0

            if j != op_num + 1:
                # 生成一个随机的符号
                self.exp_elements_infix.append(self.__rand_op(mode))
                length += 1
                # 生成随机符号之后的处理
                if have_pow and self.exp_elements_infix[length - 1] == Const.Pow:
                    # 如果刚刚生成的是乘方运算符, 且之前已经有过乘方运算符
                    self.exp_elements_infix[length - 1] = self.__rand_op(Const.Easy)
                elif have_pow is False and self.exp_elements_infix[length - 1] == Const.Pow:
                    have_pow = True

                # 随机生成左括号
                if self.exp_elements_infix[length - 1] != Const.Pow and self.exp_elements_infix[length - 1] != Const.Div:
                    # 前一个运算符不是幂运算或乘方
                    if random.randint(0, 4) == 0 and j != op_num:
                        self.exp_elements_infix.append(Const.LeftBracket)
                        left_bracket_num += 1
                        length += 1
                        last_left_bracket = 1
            else:
                while left_bracket_num > 0:
                    self.exp_elements_infix.append(Const.RightBracket)
                    length += 1
                    left_bracket_num -= 1

            if last_left_bracket != 0:
                last_left_bracket += 1
            j += 1

    def __str__(self):
        string = ""
        for element in self.exp_elements_infix:
            if element == Const.RightBracket:
                string += ")"
            elif element == Const.LeftBracket:
                string += "("
            elif element == Const.Plus:
                string += "+"
            elif element == Const.Sub:
                string += "-"
            elif element == Const.Mul:
                string += "*"
            elif element == Const.Div:
                string += "/"
            elif element == Const.Pow:
                string += "**"
            else:
                string += str(element)
        return string


i = 0
while i < 1000:
    builder = ExpressionBuilder()
    builder.build(Const.Hard)
    print(builder)
    i += 1
