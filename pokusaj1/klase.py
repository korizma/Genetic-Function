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

    def UpdateDepth(self):
        return 0
    def UpdateNodesBelow(self):
        return 0

class Constant(Function):
    def __init__(self, constant):
        self.constant = round(constant,3)

    def Kopija(self):
        return Constant(self.constant)

    def getValue(self, x):
        return f.klemp(self.constant, -granica, granica)

    def ViewF(self):
        return str(self.constant)

    def PromenaPara(self, broj):
        self.constant = broj

    def Param(self):
        return self.constant

class Variable(Function):
    def __init__(self):
        self.var = 1

    def getValue(self, x):
        return f.klemp(x, -granica, granica)

    def ViewF(self):
        return 'x'

    def Kopija(self):
        return Variable()

    def PromenaPara(self, broj):
        return

class Logarithm(Function):
    def __init__(self, base):
        self.base = abs(round(base, 3))

    def getValue(self, x):
        if x <= 0 or self.base <= 0 or self.base == 1:
            return float('NaN')
        return f.klemp(math.log(x, self.base), -granica, granica)

    def ViewF(self):
        return "log base: " + str(self.base) + " function: x"

    def Kopija(self):
        return Logarithm(self.base)

    def PromenaPara(self, broj):
        self.base = broj

    def Param(self):
        return self.base

class Exponential(Function):
    def __init__(self, base):
        self.base = abs(round(base, 3))

    def getValue(self, x):
        if x < 0:
            return float('NaN')

        elif x == 0 and self.base == 0:
            return float('NaN')

        if x > exp_granica:
            x = exp_granica

        return f.klemp(self.base ** x, -granica, granica)

    def ViewF(self):
        return str(self.base) + " to the power of: x"

    def Kopija(self):
        return Exponential(self.base)

    def PromenaPara(self, broj):
        self.base = broj

    def Param(self):
        return self.base

class NRoot(Function):
    def __init__(self, nroot):
        self.nroot = abs(int(nroot))+1

    def getValue(self, x):
        res = x ** (1 / self.nroot)

        if type(res) == type(complex(1, 1)):
            return float('NaN')
        if math.isnan(res):
            return float('NaN')

        return f.klemp(res, -granica, granica)

    def ViewF(self):
        return "the " + str(self.nroot) + " root of x"

    def Kopija(self):
        return NRoot(self.nroot)

    def PromenaPara(self, broj):
        self.nroot = broj

    def Param(self):
        return self.nroot

class Trygonometry(Function):
    def __init__(self, type):
        self.type = type

    def getValue(self, x):
        if math.isnan(x):
            return x
        if self.type == 'sin':
            x = x % (2*math.pi)
            return math.sin(x)
        elif self.type == 'cos':
            x = x % (2*math.pi)
            return math.cos(x)
        elif self.type == 'tg':
            x = x % (math.pi)
            if math.cos(x) == 0:
                return float('NaN')
            return f.klemp(math.tan(x), -granica, granica)
        elif self.type == 'ctg':
            x = x % (math.pi)
            if math.sin(x) == 0:
                return float('NaN')
            return f.klemp(math.cos(x)/math.sin(x), -granica, granica)
        else:
            return float('NaN')

    def ViewF(self):
        return self.type + "x"

    def Kopija(self):
        return Trygonometry(self.type)

    def PromenaPara(self, broj):
        return

    def PromenaTipa(self, type):
        self.type = type

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
                return f.klemp(f1.getValue(f2.getValue(x)), -granica, granica)

        if math.isnan(f1.getValue(x)) or math.isnan(f2.getValue(x)):
            return float('NaN')
        if op == '+':
            return f.klemp(f1.getValue(x) + f2.getValue(x), -granica, granica)
        elif op == '-':
            return f.klemp(f1.getValue(x) - f2.getValue(x), -granica, granica)
        elif op == '*':
            return f.klemp(f1.getValue(x) * f2.getValue(x), -granica, granica)
        elif op == '/':
            if f2.getValue(x) == 0:
                return float('NaN')
            return f.klemp(f1.getValue(x) / f2.getValue(x), -granica, granica)
        else:
            return float('NaN')

    def ViewF(self):
        return "("+self.f1.ViewF() + " " + self.op + " " + self.f2.ViewF() + ")"

    def UpdateZaKopiju(self, depth, node_below):
        self.depth = depth
        self.nodes_below = node_below

    def Kopija(self):
        b = ComplexFunction(self.f1.Kopija(), self.f2.Kopija(), self.op)
        b.UpdateZaKopiju(self.depth, self.nodes_below)
        return b

    def ChangeF1(self, f):
        self.f1 = f

    def ChangeF2(self, f):
        self.f2 = f

    def ChangeOp(self, op):
        self.op = op

    def Depth(self):
        return self.depth

    def UpdateDepth(self):
        self.depth = max(self.f1.UpdateDepth(), self.f2.UpdateDepth()) + 1
        return self.depth

    def F1(self):
        return self.f1
    def F2(self):
        return self.f2
    def Op(self):
        return  self.op

    def NodesBelow(self):
        return self.nodes_below

    def UpdateNodesBelow(self):
        self.nodes_below =  self.f1.UpdateNodesBelow() + self.f2.UpdateNodesBelow() + 2
        return self.nodes_below


