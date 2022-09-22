import math
import pandas as pd
import numpy as np
import random as rd
import klase
import expression_random as er
import copy
import parametri
import time
import ispis_logova as il
import funkcije

max_dubina = parametri.max_dubina()
mutacija_posto = parametri.mutacija_posto()
velicina_populacije = parametri.velicina_populacije()
procenat_top_jedinki = parametri.procenat_top_jedinki()
max_odstupanje = parametri.max_odstupanje()




# vraca drvo koje je mutirano na nacin koji izabere random noud i na njemu upise random drvo tako da ne predje dubinu originalnog drveta
def mutacija_boljaaa_suii(root):
    d = root.Depth()
    br_k = int(rd.uniform(0, d)+1)
    sve = vrati_random_node(root, br_k)
    f = sve[0]
    br_g = sve[1]

    do_dubine = max_dubina - br_k - 1
    # do_dubine = max(f.Depth()-1, d - br_k - 1)
    k = er.grow_metoda(do_dubine)

    if br_g == 1:
        f.ChangeF1(k)
    elif br_g == 2:
        f.ChangeF2(k)


    root.UpdateNodesBelow()
    root.UpdateDepth()
    if root.Depth() > max_dubina:
        return float('NaN')
    return root

# vraca kopiju random poddrveta kao jedinku
def mutacija_poddrvo_jedinka(root):
    nesto = vrati_random_node(root, int(rd.uniform(0, root.Depth())))
    broj = nesto[1]
    roditelj = nesto[0]

    if broj == 1:
        return roditelj.F1().Kopija()

    return roditelj.F2().Kopija()

# promeni sve parametre na random brojeve
def mutacija_randomizacija_svih_parametara(root):
    if type(root) != type(klase.ComplexFunction(1,1,1)):
        root.PromenaPara(funkcije.random_broj())
        return

    mutacija_randomizacija_svih_parametara(root.F1())
    mutacija_randomizacija_svih_parametara(root.F2())

# vraca roditelja tog nouda i da li je f1 ili f2
def vrati_random_node(root, broj_koraka):
    vf1 = root.F1().NodesBelow() + 1
    vf2 = root.F2().NodesBelow() + 1
    vrv = vf1 / (vf1 + vf2)

    rnd_broj = rd.uniform(0,1)

    if broj_koraka == 1:
        if rnd_broj < vrv:
            return [root, 1]
        else:
            return [root, 2]

    if rnd_broj < vrv:
        if type(root.F1()) == type(klase.ComplexFunction(1, 1, 1)):
            return vrati_random_node(root.F1(), broj_koraka - 1)
        else:
            return [root, 1]
    else:
        if type(root.F2()) == type(klase.ComplexFunction(1, 1, 1)):
            return vrati_random_node(root.F2(), broj_koraka - 1)
        else:
            return [root, 2]

# zameni dva poddrva tako da nijedna novo napravljena jedina ne predje dubinu roditelja
def crossover_drva(root1, root2):
    d1 = root1.Depth()
    d2 = root2.Depth()

    if d1 < d2:
        pom = root1
        root1 = root2
        root2 = pom
        d1 = root1.Depth()
        d2 = root2.Depth()

    br1 = int(rd.uniform(d1-d2, root1.Depth())+1)
    br2 = int(rd.uniform(d2-d1+br1, d2)+1)
    pom1 = vrati_random_node(root1, br1)
    pom2 = vrati_random_node(root2, br2)

    node1 = pom1[0]
    node2 = pom2[0]
    f1 = pom1[1]
    f2 = pom2[1]

    if f1 == 1 and f2 == 1:
        pom = node1.F1()
        node1.ChangeF1(node2.F1())
        node2.ChangeF1(pom)

    elif f1 == 2 and f2 == 1:
        pom = node1.F2()
        node1.ChangeF2(node2.F1())
        node2.ChangeF1(pom)

    elif f1 == 1 and f2 == 2:
        pom = node1.F1()
        node1.ChangeF1(node2.F2())
        node2.ChangeF2(pom)

    elif f1 == 2 and f2 == 2:
        pom = node1.F2()
        node1.ChangeF2(node2.F2())
        node2.ChangeF2(pom)

    root1.UpdateDepth()
    root2.UpdateDepth()
    root1.UpdateNodesBelow()
    root2.UpdateNodesBelow()

    return [root1, root2]

def rulet_mutacija_crossover(ftns, broj_jedinki):
    new_pop = []
    br_m = int(broj_jedinki*mutacija_posto)
    br_c = broj_jedinki - br_m

    suma = sum((max_odstupanje - i) for i in ftns["fitness"])

    for i in range(br_m):
        tree = random_index_wheel(ftns, suma)     #dasdasdasdsa
        mutirano = float("NaN")
        while type(mutirano) != type(klase.ComplexFunction(1,1,1)):
            mutirano = mutacija_boljaaa_suii(tree)
        new_pop.append(mutirano.Kopija())



    while br_c != 0:
        tree1 = random_index_wheel(ftns, suma)    #dasdasdasdsa
        tree2 = random_index_wheel(ftns, suma)    #dasdasdasdsa

        d1 = tree1
        d2 = tree2

        sve = crossover_drva(d1, d2)
        for i in sve:
            new_pop.append(i.Kopija())
            br_c -= 1
    return new_pop

# izabera random funkciju iz populacije i ako je u top jedinikama vrati njihovu kopiju
def random_index_wheel(ftns, s):
    r = rd.uniform(0,s)
    rx = 0
    pom = 0
    for i in range(0, len(ftns["func"])):
        rx += max_odstupanje - ftns["fitness"][i]
        if rx >= r:
            f = ftns['func'][i]
            pom = i

    if i < velicina_populacije * procenat_top_jedinki:
        return kopija(f)
    return f

def kopija(func):
    return func.Kopija()

def pravljenje_nove_generacije(populacija, broj_jedinki):
    new_pop = []
    br_m = int(broj_jedinki * mutacija_posto)
    br_c = broj_jedinki - br_m

    suma = sum((max_odstupanje - i) for i in populacija["fitness"])

    random_jedinke = int(br_m * 0.25)
    random_parametri = int(br_m * 0.25)
    random_poddrvo_jedinka = int(br_m * 0.25)
    random_podrvo_randomizuj = int(br_m - 3 * int(br_m * 0.25))

    for i in range(random_jedinke):
        new_pop.append(er.grow_metoda(max_dubina).Kopija())

    for i in range(random_parametri):
        tree = random_index_wheel(populacija, suma)
        mutacija_randomizacija_svih_parametara(tree)
        new_pop.append(tree.Kopija())

    for i in range(random_poddrvo_jedinka):
        tree = random_index_wheel(populacija, suma)
        new_pop.append(mutacija_poddrvo_jedinka(tree).Kopija())

    for i in range(random_podrvo_randomizuj):
        tree = random_index_wheel(populacija, suma)  # dasdasdasdsa
        mutirano = float("NaN")
        while type(mutirano) != type(klase.ComplexFunction(1, 1, 1)):
            mutirano = mutacija_boljaaa_suii(tree)
        new_pop.append(mutirano.Kopija())

    while br_c >= 0:
        tree1 = random_index_wheel(populacija, suma)  # dasdasdasdsa
        tree2 = random_index_wheel(populacija, suma)  # dasdasdasdsa

        d1 = tree1
        d2 = tree2

        sve = crossover_drva(d1, d2)
        for i in sve:
            new_pop.append(i.Kopija())
            br_c -= 1

    return new_pop


