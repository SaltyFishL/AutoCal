from src.Const import Const
from src.ExpressionBuilder import ExpressionBuilder
from src.BinaryTree import BinaryTree
from src.Num import Num


def build_exps(max_exp_num, mode):
    i = 1
    exp_file = open("../res/expressions.txt", "w")
    ans_file = open("../res/answer.txt", "w")
    is_new = True
    expressions = []
    while i <= max_exp_num:
        builder = ExpressionBuilder()
        builder.build(mode)
        is_new = True
        for expression in expressions:
            assert isinstance(expression, ExpressionBuilder)
            assert isinstance(expression.tree, BinaryTree)
            if expression.tree.is_same_tree(builder.tree):
                is_new = False
                break
        if is_new:
            expressions.append(builder)
            exp_file.write(str(i) + ". " + str(builder) + '\n')
            assert isinstance(builder.ans, Num)
            if mode == Const.Easy:
                ans_file.write(str(i) + ". "
                               + "{:.2f}".format(builder.ans.numerator / builder.ans.denominator * builder.ans.sign)
                               + '\n')
            else:
                ans_file.write(str(i) + ". ")
                ans_file.write(str(builder.ans) + '\n')
        else:
            i -= 1
        i += 1
    exp_file.close()
    ans_file.close()


def main():
    # try:
    #     max_exp_num = int(input("请输入1000以内需要的题目数量: "))
    #     mode = int(input("请输入生成题目的类型编号(1.整数四则运算 2.分数四则运算 3.分数带乘方运算): "))
    #     if mode == 1:
    #         mode = Const.Easy
    #     elif mode == 2:
    #         mode = Const.Medium
    #     elif mode == 3:
    #         mode = Const.Hard
    #     else:
    #         raise ValueError
    #     build_exps(max_exp_num, mode)
    # except ValueError:
    #     print("输入数字错误")
    build_exps(1000, Const.Hard)


if __name__ == '__main__':
    main()