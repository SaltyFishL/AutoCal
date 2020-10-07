import random
from src.Const import Const
from src.Stack import Stack
from src.Num import Num
from src.BinaryTree import BinaryTree
from src.BinaryTree import Node
from src.BinaryTree import cal


class ExpressionBuilder:
    def __init__(self):
        self.exp_elements_infix = []
        self.exp_elements_suffix = []
        self.tree = None
        self.ans = None

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

    @staticmethod
    def __rand_op_num():
        return random.randint(1, 10)

    @staticmethod
    def __rand_op(mode):
        """mode为Easy时, 整数加减乘除; mode为Medium时, 加分数; mode为Hard时, 加乘方"""
        if mode == Const.Easy:
            return random.randint(Const.Plus, Const.Sub)
        if mode == Const.Medium:
            return random.randint(Const.Plus, Const.Div)
        if mode == Const.Hard:
            return random.randint(Const.Plus, Const.Pow)

    @staticmethod
    def __rand_num():
        return random.randint(0, 100)

    @staticmethod
    def __rand_pow_num():
        return random.randint(1, 3)

    def build_exp_infix(self, mode):
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
            if length > 1 and self.exp_elements_infix[length - 2] in range(Const.LeftBracket, Const.RightBracket + 1):
                if random.randint(0, 2) == 0:
                    self.exp_elements_infix[length - 1] *= -1
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

    def infix_to_suffix(self):
        op_stack = Stack()
        for element in self.exp_elements_infix:
            if element == Const.Pow or element == Const.LeftBracket:
                # 左括号和乘方必定入栈
                op_stack.push(element)
            elif element == Const.Mul or element == Const.Div:
                # 乘除法需要弹出乘方与乘除
                while op_stack.size() > 0 and \
                        (op_stack.peek() == Const.Mul or op_stack.peek() == Const.Div or op_stack.peek() == Const.Pow):
                    op = op_stack.pop()
                    self.exp_elements_suffix.append(op)
                op_stack.push(element)
            elif element == Const.Plus or element == Const.Sub:
                while op_stack.size() > 0 and (op_stack.peek() != Const.LeftBracket):
                    op = op_stack.pop()
                    self.exp_elements_suffix.append(op)
                op_stack.push(element)
            elif element == Const.RightBracket:
                while op_stack.peek() != Const.LeftBracket:
                    op = op_stack.pop()
                    self.exp_elements_suffix.append(op)
                op_stack.pop()
            else:
                self.exp_elements_suffix.append(element)
        while op_stack.size() > 0:
            self.exp_elements_suffix.append(op_stack.pop())

    def suffix_to_tree(self):
        node_stack = Stack()
        op_num = 0
        for elm in self.exp_elements_suffix:
            node = Node()
            if elm < Const.Min:
                node.type = Const.NumNode
                node.num = Num(elm)
            else:
                op_num += 1
                node.type = Const.OpNode
                node.right = node_stack.pop()
                node.left = node_stack.pop()
                node.op = elm
            node_stack.push(node)
        self.tree = BinaryTree(node_stack.pop(), op_num)

    def get_ans(self):
        assert isinstance(self.tree, BinaryTree), "表达式树不为BinaryTree"
        self.ans = self.tree.cal()

    def build(self, mode):
        self.build_exp_infix(mode)
        self.infix_to_suffix()
        self.suffix_to_tree()
        self.get_ans()
        assert isinstance(self.tree, BinaryTree)
        self.tree.adjust_tree(self.tree.root)


def main():
    index = 0
    while index < 1000:
        builder = ExpressionBuilder()
        builder.build(Const.Hard)
        print(builder)

        # string = ""
        # for element in builder.exp_elements_suffix:
        #     if element == Const.RightBracket:
        #         string += ")"
        #     elif element == Const.LeftBracket:
        #         string += "("
        #     elif element == Const.Plus:
        #         string += "+"
        #     elif element == Const.Sub:
        #         string += "-"
        #     elif element == Const.Mul:
        #         string += "*"
        #     elif element == Const.Div:
        #         string += "/"
        #     elif element == Const.Pow:
        #         string += "**"
        #     else:
        #         string += str(element)
        # print(string)
        index += 1


if __name__ == '__main__':
    main()
