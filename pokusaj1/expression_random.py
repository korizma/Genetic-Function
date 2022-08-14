import math
import random
import klase
import funkcije as f
import time

p = 0.8     #pocetna verovatnoca za grananje u half half algoritmu
q = 0.9     #procentaza opada verovatnoce za grananje half half algoritmu
sansa_pom = p / q

verovatnoce_za_operacije = [0.2, 0.2, 0.2, 0.2, 0.2]            #+ - * / o
verovatnoce_za_funkcije = [0.3, 0.14, 0.14, 0.14, 0.14, 0.14]   #konst variable log nroot exp trygon

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
    broj = random.randint(0, 7)
    if broj <= 2:
        return klase.Constant(f.random_broj())
    elif broj  <= 3:
        return klase.Variable()
    elif broj == 4:
        return klase.Logarithm(f.random_broj())
    elif broj == 5:
        return klase.NRoot(f.random_broj())
    elif broj == 6:
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
    global p, q, sansa_pom

    sansa_pom *= q

    glavna = klase.ComplexFunction(1, 1, generisi_random_op())

    if dubina == 0:
        nastavlja_se = False
    else:
        nastavlja_se = True

    if random.uniform(0,1) < sansa_pom and nastavlja_se:
        glavna.ChangeF1(generisi_random_funkciju_tree(dubina-1))
        nastavlja_se = True
    else:
        glavna.ChangeF1(generisi_random_funkciju())

    if random.uniform(0,1) < sansa_pom and nastavlja_se:
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
    br_y = int((num_nodes - 3) / 2)
    br_x = num_nodes - 3

    pre = "xx"
    post = "xyy"



    lista_mesta_yy = [False for i in range(br_x)]
    proslo = 0
    stek = 2
    preskace = 0

    for a in range(1, br_y+1):
        if stek >= 2:
            preskace = 0
        else:
            preskace = 2 - stek

        mesto = random.randint(proslo + 1 + preskace, br_x - (br_y - a))
        lista_mesta_yy[mesto-1] = True
        stek -= 2
        stek += 1

        stek += mesto - proslo - 1
        proslo = mesto


    word = pre
    for tu_je in lista_mesta_yy:
        word += "x"
        if tu_je:
            word += "yy"

    word += post
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
            stek = stek[0:len(stek)-2]
            stek.append(non_terminal)
            i += 3
        else:
            terminal = napravi_terminali_node()
            stek.append(terminal)
            i += 1
    
    return non_terminal

for i in range(50):
    word = generisi_dyck_word(9)
    stablo = napravi_stablo(word)
    print(stablo.ViewF())