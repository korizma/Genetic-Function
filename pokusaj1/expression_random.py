import math
import random
import klase
import funkcije as f

def generisi_random_op():
    op_broj = random.randint(0,4)
    if op_broj == 0:
        return "+"
    elif op_broj == 1:
        return "-"
    elif op_broj == 2:
        return "*"
    elif op_broj == 3:
        return "/"
    return "o"

def generisi_random_funkciju():
    broj = random.randint(0, 10)
    if broj <= 4:
        return klase.Constant(f.random_broj())
    elif broj  <= 6:
        return klase.Variable()
    elif broj == 7:
        return klase.Logarithm(f.random_broj())
    elif broj == 8:
        return klase.NRoot(f.random_broj())
    elif broj == 9:
        return klase.Exponential(f.random_broj())

    broj = random.randint(0, 3)
    if broj == 0:
        return  klase.Trygonometry("sin")
    elif broj == 1:
        return  klase.Trygonometry("cos")
    elif broj == 2:
        return  klase.Trygonometry("tg")
    elif broj == 3:
        return  klase.Trygonometry("ctg")

def generisi_random_funkciju_tree(dubina):
    glavna = klase.ComplexFunction(1, 1, generisi_random_op())
    if dubina > 0:
        nastavlja_se = True
    if dubina == 0:
        nastavlja_se = False

    if random.uniform(0,1) < 0.5 and nastavlja_se:
        glavna.ChangeF1(generisi_random_funkciju_tree(dubina-1))
        nastavlja_se = True
    else:
        glavna.ChangeF1(generisi_random_funkciju())

    if random.uniform(0,1) < 0.5 and nastavlja_se:
        glavna.ChangeF2(generisi_random_funkciju_tree(dubina-1))
        nastavlja_se = True
    else:
        glavna.ChangeF2(generisi_random_funkciju())

    return  glavna


for x in range(100):
    print(generisi_random_funkciju_tree(7).ViewF())