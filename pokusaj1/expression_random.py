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

"""
for x in range(1000000):
    m = generisi_random_funkciju_tree(7)
    print(m.ViewF())
    if (m.GetDepth() > 8):
        print("uzasssss")
        break
   """

#dyck word random tree

#broj nodudova mora biti neparan
def generisi_dyck_word(num_nodes):
    l = int((num_nodes - 1) / 2)
    rs = (num_nodes + 1) / 2

    cn = math.factorial(num_nodes-1) / (math.factorial(l) * math.factorial(rs))

    print("broj razlicitih struktura tree-a: " + str(cn))

    prosla_pos = 2

    yy_pozicije = [False for x in range(num_nodes)]
    for i in range(l):
        yy_pos = random.randint(prosla_pos+1, num_nodes - l + i)
        prosla_pos = yy_pos
        yy_pozicije[yy_pos] = True

    word = ""
    for pozicija in yy_pozicije:
        word += "x"
        if pozicija:
            word += "yy"
    return word

#pretvaranje dyck reci u tree

def napravi_terminali_node():
    return generisi_random_funkciju()
def napravi_neterminalni_node(f1, f2):
    return klase.ComplexFunction(f1, f2, generisi_random_op())

def napravi_stablo(word):
    stek = []
    duzina_reci = len(word)
    i = 0

    non_terminal = 1
    terminal = 1

    while i < duzina_reci:
        if word[i+1] == 'y':
            non_terminal = napravi_neterminalni_node(stek[len(stek)-1], stek[len(stek)-2])
            stek = stek[:-2]
            stek.append(non_terminal)
            i += 3
        else:
            terminal = napravi_terminali_node()
            stek.append(terminal)
            i += 1

    print(non_terminal.ViewF())



word = generisi_dyck_word(9)
print(word)
napravi_stablo(word)
