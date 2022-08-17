import math
import funkcije as f
import parametri

granica = parametri.granica_klase()
exp_granica = parametri.exp_granica_klase()

class Function:
    def getValue(self, x):
        return 0

    def ViewF(self):
        return "a"

    def Depth(self):
        self.depth = 0
        return self.depth

    def NodesBelow(self):
        return 0

class Constant(Function):
    def __init__(self, constant):
        self.constant = round(constant,3)

    def getValue(self, x):
        return f.clamp(self.constant, -granica, granica)

    def ViewF(self):
        return str(self.constant)

class Variable(Function):
    def __init__(self):
        self.var = 1

    def getValue(self, x):
        return f.clamp(x, -granica, granica)

    def ViewF(self):
        return 'x'

class Logarithm(Function):
    def __init__(self, base):
        self.base = abs(round(base, 3))

    def getValue(self, x):
        if x <= 0 or self.base <= 0 or self.base == 1:
            return float('NaN')
        return f.clamp(math.log(x, self.base), -granica, granica)

    def ViewF(self):
        return "log base: " + str(self.base) + " function: x"

class Exponential(Function):
    def __init__(self, base):
        self.base = abs(round(base, 3))

    def getValue(self, x):
        if x < 0:
            return float('NaN')
        if x == 0 and self.base == 0:
            return float('NaN')
        if x > exp_granica:
            x = exp_granica
        return f.clamp(self.base ** x, -granica, granica)

    def ViewF(self):
        return str(self.base) + " to the power of: x"

class NRoot(Function):
    def __init__(self, nroot):
        self.nroot = abs(int(nroot))+1

    def getValue(self, x):
        res = x ** (1 / self.nroot)

        if type(res) == type(complex(1, 1)):
            return float('NaN')
        if math.isnan(res):
            return float('NaN')

        return f.clamp(res, -granica, granica)

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
                return float('NaN')
            return f.clamp(math.tan(x), -granica, granica)
        elif self.type == 'ctg':
            if math.sin(x) == 0:
                return float('NaN')
            return f.clamp(math.cos(x)/math.sin(x), -granica, granica)
        else:
            return "Undefined Type"

    def ViewF(self):
        return self.type + "x"

class ComplexFunction(Function):
    def __init__(self, f1, f2, op):
        self.f1 = f1
        self.f2 = f2
        self.op = op
        self.depth = 0
        self.nodes_below = 0
    def getValue(self, x):
        op = self.op
        f1 = self.f1
        f2 = self.f2
        if op == 'o':
            if math.isnan(f2.getValue(x)):
                return float('NaN')
            else:
                return f.clamp(f1.getValue(f2.getValue(x)), -granica, granica)

        if math.isnan(f1.getValue(x)) or math.isnan(f2.getValue(x)):
            return float('NaN')
        if op == '+':
            return f.clamp(f1.getValue(x) + f2.getValue(x), -granica, granica)
        elif op == '-':
            return f.clamp(f1.getValue(x) - f2.getValue(x), -granica, granica)
        elif op == '*':
            return f.clamp(f1.getValue(x) * f2.getValue(x), -granica, granica)
        elif op == '/':
            if f2.getValue(x) == 0:
                return float('NaN')
            return f.clamp(f1.getValue(x) / f2.getValue(x), -granica, granica)
        else:
            return "Something is wrong"

    def ViewF(self):
        if self.op == "o":
            izgled_f1 = self.f1.ViewF()
            izgled_f1 = izgled_f1[0:len(izgled_f1)-2]
            return izgled_f1 + "(" + self.f2.ViewF() + ")"
        else:
            return "("+self.f1.ViewF() + ") " + self.op + " (" + self.f2.ViewF() + ")"

    def ChangeF1(self, f):
        self.f1 = f

    def ChangeF2(self, f):
        self.f2 = f

    def ChangeOp(self, op):
        self.op = op

    def Depth(self):
        return self.depth

    def UpdateDepth(self):
        self.depth = max(self.f1.Depth(), self.f2.Depth()) + 1

    def F1(self):
        return self.f1
    def F2(self):
        return self.f2
    def Op(self):
        return  self.op

    def NodesBelow(self):
        return self.nodes_below

    def UpdateNodesBelow(self):
        self.nodes_below =  self.f1.NodesBelow() + self.f2.NodesBelow() + 2