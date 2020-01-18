
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

    def __add__(self, other):
        assert isinstance(other, Num) , "加法右边类型不为Num"
        res = Num()
        if self.sign * other.sign == 1:
            if self.sign == 1 and other.sign == 1:
                # + + +
                res.sign = 1
            else:
                # - + -
                res.sign = -1
            res.numerator = self.numerator * other.denominator + self.denominator * other.numerator
            res.denominator = self.denominator * other.denominator
            res.reduction()
        else:
            if self.sign == 1 and other.sign == -1:
                # + + -
                res.numerator = self.numerator * other.denominator - self.denominator * other.numerator
                res.denominator = self.denominator * other.denominator
            else:
                # - + +
                res.numerator = other.numerator * self.denominator - other.denominator * self.numerator
                res.denominator = other.denominator * self.denominator
            res.reduction()
        return res

    def __sub__(self, other):
        assert isinstance(other, Num), "减法右边类型不为Num"
        res = Num()
        if self.sign * other.sign == 1:
            if self.sign == 1 and other.sign == 1:
                # + - +
                res.sign = 1
            else:
                # - - -
                res.sign = -1
            res.numerator = self.numerator * other.denominator - self.denominator * other.numerator
            res.denominator = self.denominator * other.denominator
            res.reduction()
        else:
            if self.sign == 1 and other.sign == -1:
                # + - -
                res.sign = 1
            else:
                # - - +
                res.sign = -1
            res.numerator = self.numerator * other.denominator + self.denominator * other.numerator
            res.denominator = self.denominator * other.denominator
            res.reduction()
        return res

    def __mul__(self, other):
        assert isinstance(other, Num), "乘法右边类型不为Num"
        res = Num(self.numerator * other.numerator, self.denominator * other.denominator, self.sign * other.sign)
        res.reduction()
        return res

    def __truediv__(self, other):
        assert isinstance(other, Num) , "除法右边类型不为Num"
        res = Num(self.numerator * other.denominator, self.denominator * other.numerator, self.sign * other.sign)
        res.reduction()
        return res

    def __pow__(self, power, modulo=None):
        assert isinstance(power, Num), "乘方幂类型不为Num"
        res = Num(1)
        i = 0
        while i < power.numerator:
            res.denominator *= self.denominator
            res.numerator *= self.numerator
            res.sign *= self.sign
            i += 1
        res.reduction()
        return res

    def __eq__(self, other):
        assert isinstance(other, Num), "==右边不为Num"
        if self.sign == other.sign and self.numerator == other.numerator and self.denominator == other.denominator:
            return True
        else:
            return False

    def __lt__(self, other):
        assert isinstance(other, Num), "<右边不为Num"
        return self.sign * self.numerator / self.denominator < other.sign * other.numerator / other.denominator

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


def main():
    a = Num(1, 2)
    b = Num(5)
    print(a + b)
    print(b - a)
    print(a * b)
    print(a / b)
    print(a ** b)
    c = Num(4, 5, -1)
    print(a + c)
    print(a - c)
    print(a * c)
    print(a / c)
    print(c ** b)
    print(a < b)
    print(b < a)
    print(c < a)
    print(a == b)


if __name__ == '__main__':
    main()
