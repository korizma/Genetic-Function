import math
import pandas as pd
import numpy as np
import random as rd
import klase
import expression_random as er
import copy
import parametri
import time

max_dubina = parametri.max_dubina()
mutacija_posto = parametri.mutacija_posto()

def mutacija_rnd_tree(root, broj_koraka, max_depth_rnd_drveta):
    vf1 = root.F1().NodesBelow() + 1
    vf2 = root.F2().NodesBelow() + 1
    vrv = vf1 /(vf1+vf2)

    rnd_br = rd.uniform(0,1)

    if broj_koraka == 1:
        if rnd_br < vrv:
            root.ChangeF1(er.grow_metoda(max_depth_rnd_drveta-1))             #ovde ide random f_ja
            return
        else:
            root.ChangeF2(er.grow_metoda(max_depth_rnd_drveta-1))             #ovde ide random f_ja
            return

    if rnd_br < vrv:
        if type(root.F1()) == type(klase.ComplexFunction(1,1,1)):
            mutacija_rnd_tree(root.F1(), broj_koraka-1, max_depth_rnd_drveta-1)
        else:
            root.ChangeF1(er.generisi_random_funkciju())
    else:
        if type(root.F2()) == type(klase.ComplexFunction(1, 1, 1)):
            mutacija_rnd_tree(root.F2(), broj_koraka - 1, max_depth_rnd_drveta - 1)
        else:
            root.ChangeF2(er.generisi_random_funkciju())

def mutacija_boljaaa_suii(root):
    d = root.Depth()
    br_k = int(rd.uniform(0, d)+1)
    sve = vrati_random_node(root, br_k)
    f = sve[0]
    br_g = sve[1]

    if br_g == 1:
        f.ChangeF1(er.grow_metoda(d-br_k))
    elif br_g == 2:
        f.ChangeF2(er.grow_metoda(f.Depth()-1))

    root.UpdateNodesBelow()
    root.UpdateDepth()

    return root

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
            return vrati_random_node(root.F1(), broj_koraka-1)
        else:
            return [root, 1]
    else:
        if type(root.F2()) == type(klase.ComplexFunction(1, 1, 1)):
            return vrati_random_node(root.F2(), broj_koraka - 1)
        else:
            return [root, 2]

def crossover_drva(root1, root2):
    global max_dubina
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

    suma = sum((max_dubina/i) for i in ftns["fitness"])
    print(suma)
    start = time.time()
    for i in range(br_m):
        tree = random_index_wheel(ftns, suma)     #dasdasdasdsa
        tree = mutacija_boljaaa_suii(tree)
        new_pop.append(tree)

    print("mutiranje je trajalo: " + str(time.time() - start) + "s")

    start = time.time()

    while br_c != 0:
        tree1 = random_index_wheel(ftns, suma)    #dasdasdasdsa
        tree2 = random_index_wheel(ftns, suma)    #dasdasdasdsa

        d1 = tree1
        d2 = tree2

        sve = crossover_drva(d1, d2)
        for i in sve:
            new_pop.append(i)
        br_c -= 1

    print("crossover je trajao: " + str(time.time() - start) + "s")
    return new_pop[0:broj_jedinki]

def random_index_wheel(ftns, s):
    r = rd.uniform(0,s)
    rx = 0
    for i in range(0, len(ftns["func"])):
        rx += max_dubina/ftns["fitness"][i]
        if rx >= r:
            fff = ftns['func'][i]
            return fff

