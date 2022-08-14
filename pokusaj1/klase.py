import math

class Function:
    def getValue(self, x):
        return 0

    def ViewF(self):
        return "a"

    def Height(self):
        return 0

    def Depth(self, parent_depth):
        self.depth = parent_depth + 1
        return self.depth

class Constant(Function):
    def __init__(self, constant):
        self.constant = round(constant,3)

    def getValue(self, x):
        return self.constant

    def ViewF(self):
        return str(self.constant)

class Variable(Function):
    def __init__(self):
        self.var = 1

    def getValue(self, x):
        return x

    def ViewF(self):
        return 'x'

class Logarithm(Function):
    def __init__(self, base):
        self.base = abs(round(base, 3))

    def getValue(self, x):
        if x <= 0 or self.base <= 0 or self.base == 1:
            return NaN
        return math.log(x, self.base)

    def ViewF(self):
        return "log base: " + str(self.base) + " function: x"

class Exponential(Function):
    def __init__(self, base):
        self.base = abs(round(base, 3))

    def getValue(self, x):
        if x < 0:
            return NaN
        if x == 0 and self.base == 0:
            return NaN
        return self.base ** x

    def ViewF(self):
        return str(self.base) + " to the power of: x"

class NRoot(Function):
    def __init__(self, nroot):
        self.nroot = abs(int(nroot))

    def getValue(self, x):
        if self.nroot % 2 == 0 and x < 0:
            return NaN
        if self.nroot == 0:
            return NaN
        return x ** (1/self.nroot)

    def ViewF(self):
        return "the " + str(self.nroot) + " root of x"

class Trygonometry(Function):
    def __init__(self, type):
        self.type = type

    def getValue(self, x):
        if self.type == 'sin':
            return math.sin(x)
        elif self.type == 'cos':
            return math.cos(x)
        elif self.type == 'tg':
            if math.cos(x) == 0:
                return NaN
            return math.tan(x)
        elif self.type == 'ctg':
            if math.sin(x) == 0:
                return NaN
            return math.cos(x)/math.sin(x)
        else:
            return "Undefined Type"

    def ViewF(self):
        return self.type + "x"

class ComplexFunction(Function):
    def __init__(self, f1, f2, op):
        self.f1 = f1
        self.f2 = f2
        self.op = op
    def getValue(self, x):
        op = self.op
        f1 = self.f1
        f2 = self.f2
        if op == 'o':
            if f2.getValue(x) == NaN:
                return Nan
            else:
                return f1.getValue(f2.getValue(x))

        if f1.getValue(x) == NaN or f2.getValue(x) == NaN:
            return NaN
        if op == '+':
            return f1.getValue(x) + f2.getValue(x)
        elif op == '-':
            return f1.getValue(x) - f2.getValue(x)
        elif op == '*':
            return f1.getValue(x) * f2.getValue(x)
        elif op == '/':
            if f2.getValue(x) == 0:
                return NaN
            return f1.getValue(x) / f2.getValue(x)
        else:
            return "Something is wrong"

    def ViewF(self):
        if op == "o":
            izgled_f1 = f1.ViewF()
            izgled_f1 = izgled_f1[0:len(izgled_f1-2)]
            return izgled_f1 + "(" + f2.ViewF() + ")"
        else:
            return "("+self.f1.ViewF() + ") " + self.op + " (" + self.f2.ViewF() + ")"

    def ChangeF1(self, f):
        self.f1 = f

    def ChangeF2(self, f):
        self.f2 = f

    def ChangeOp(self, op):
        self.op = op

    def Height(self):
        self.height = max(f1.Height(), f2.Height())
        return self.height

    def Depth(self, tree_depth):
        self.depth = tree_depth - self.height
        self.f1.Depth(tree_depth - 1)