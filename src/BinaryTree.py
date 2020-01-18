from src.Num import Num
from src.Const import Const


def compare_node(node1, node2):
    assert isinstance(node1, Node)
    assert isinstance(node2, Node)
    if node1.type != node2.type:
        return False
    else:
        left_same = False
        right_same = False
        if node1.left is not None and node2.left is not None:
            left_same = compare_node(node1.left, node2.left)
        if node1.right is not None and node2.right is not None:
            right_same = compare_node(node1.right, node2.right)
        if left_same and right_same and node1.num == node2.num:
            return True
        return False


def cal(node):
    if node.type == Const.OpNode:
        num1 = cal(node.left)
        num2 = cal(node.right)
        if node.op == Const.Plus:
            node.num = num1 + num2
        elif node.op == Const.Sub:
            node.num = num1 - num2
        elif node.op == Const.Mul:
            node.num = num1 * num2
        elif node.op == Const.Div:
            node.num = num1 / num2
        elif node.op == Const.Pow:
            node.num = num1 ** num2
        else:
            raise ValueError
        return node.num
    elif node.type == Const.NumNode:
        return node.num


class Node:
    """Expression二叉树上每一个节点"""

    def __init__(self):
        self.type = None
        self.op = None
        self.num = None
        self.left = None
        self.right = None


class BinaryTree:
    """每个节点上或是运算符或是Num"""

    def __init__(self, root, op_num):
        self.root = root
        self.op_num = op_num  # 表达式运算符数量

    def adjust_tree(self, root):
        """调整为左子树永远比右子树大"""
        if root.left is not None:
            self.adjust_tree(root.left)
        if root.right is not None:
            self.adjust_tree(root.right)
        if root.left is not None and root.right is not None:
            if root.left.num < root.right.num:
                tmp = root.right
                root.right = root.left
                root.left = tmp

    def is_same_tree(self, other):
        assert isinstance(other, BinaryTree)
        if self.op_num != other.op_num:
            # 比较运算符数量
            return False
        if compare_node(self.root, other.root) is not True:
            return False
        return True

    def cal(self):
        return cal(self.root)
