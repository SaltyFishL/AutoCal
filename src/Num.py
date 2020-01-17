
class Num:
    """用来表示表达式中数字的类"""

    def __init__(self, numerator=0, denominator=1, sign=1, gcd=1):
        self.numerator = numerator  # 分子
        self.denominator = denominator    # 分母
        self.sign = sign  # 1: 正数, -1: 负数
        self.gcd = gcd
        self.reduction()

    def __str__(self):
        res = ""
        if self.sign == -1:
            res += "-"
        res += str(int(self.numerator / self.gcd))
        if self.denominator / self.gcd != 1:
            res += "/"
            res += str(int(self.denominator / self.gcd))
        return res

    def __gcd(self, x, y):
        if x < y:
            x, y = y, x
        if x % y == 0:
            return y
        else:
            return self.__gcd(y, x % y)

    def reduction(self):
        if self.numerator != 0:  # 分子不为0
            self.sign = self.sign * (self.numerator / abs(self.numerator)) * (self.denominator / abs(self.denominator))
            self.gcd = self.__gcd(abs(self.numerator), abs(self.denominator))
            self.numerator = abs(self.numerator) / self.gcd
            self.denominator = abs(self.denominator) / self.gcd
        else:
            self.denominator = 1
            self.gcd = 1
            self.sign = 1

    # TODO 这里的加减乘除均只考虑了正数
    def __add__(self, other):
        try:
            if not isinstance(other, Num):
                raise NameError
        except NameError:
            print("加法运算数不为Num类型")

        res = Num()
        res.numerator = self.numerator * other.denominator + self.denominator * other.numerator
        res.denominator = self.denominator * other.denominator
        res.reduction()
        return res

    def __sub__(self, other):
        try:
            if not isinstance(other, Num):
                raise NameError
        except NameError:
            print("减法运算数不为Num类型")
        res = Num()
        res.numerator = self.numerator * other.denominator - self.denominator * other.numerator
        res.denominator = self.denominator * other.denominator
        res.reduction()
        return res

    def __mul__(self, other):
        try:
            if not isinstance(other, Num):
                raise NameError
        except NameError:
            print("乘法运算数不为Num类型")
        return Num(self.numerator * other.numerator, self.denominator, other.denominator)

    def __truediv__(self, other):
        try:
            if not isinstance(other, Num):
                raise NameError
        except NameError:
            print("除法右运算数不为Num类型")
        return Num(self.numerator * other.denominator, self.denominator * other.numerator)

    def __pow__(self, power, modulo=None):
        try:
            if not isinstance(power, Num):
                raise NameError
        except NameError:
            print("幂运算右运算数不为Num类型")
        res = Num(1)
        i = 0
        while i < power.numerator:
            res.denominator *= self.denominator
            res.numerator *= self.numerator
            i += 1
        res.reduction()
        return res


def main():
    a = Num(1, 2)
    b = Num(5)
    print(a + b)
    print(b - a)
    print(a * b)
    print(a / b)
    print(a ** b)


if __name__ == '__main__':
    main()
