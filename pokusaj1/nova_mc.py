import math
import pandas as pd
import numpy as np
import random as rd
import klase
import expression_random as er
import copy
import parametri
import time
import ispis_logova1 as il
import funkcije

# <editor-fold desc="Parametri">
max_dubina = parametri.max_dubina()
mutacija_posto = parametri.mutacija_posto()
velicina_populacije = parametri.velicina_populacije()
procenat_top_jedinki = parametri.procenat_top_jedinki()
max_odstupanje = parametri.max_odstupanje()
sansa_promene_trigonometrije = parametri.sansa_promene_trigonometrije()
vrv_operacija = parametri.vrv_operacija()

nv_centar = parametri.nv_centar()
nv_lambda = parametri.nv_lambda()
k = parametri.k()

verovatnoca_mutacija = parametri.verovatnoca_mutacija()
# </editor-fold>

def totalno_nova_generacija(df, generacija):
    global velicina_populacije

    populacija             = []

    for i in range(int(velicina_populacije*0.1)):
        populacija.append(er.grow_metoda(max_dubina))

    prosek                 = trimmed_mean(df["fitness"])
    standard_deviation     = np.std(df["fitness"])
    niz_roditelja          = [0 for i in range(int(velicina_populacije))]
    il.log("standarnda devijacija " + str(generacija) + ". generacije je: " +str(standard_deviation) + '\n', "standard_deviation")

    # niz_vrv_rulet = []
    # suma_vrv = 0
    # h = velicina_populacije
    # for i in range(int(velicina_populacije/2)):
    #     niz_vrv_rulet.append(h+0)
    #     suma_vrv += h
    #     h /= k

    vrv_c = 0 + standard_deviation/50 * 0.18
    vrv_m = 1 - standard_deviation/50 * 0.1

    # if standard_deviation < 30:
    #     vrv_c = 0.1
    #     vrv_m = 1
    # elif standard_deviation < 40:
    #     vrv_c = 0.3
    #     vrv_m = 0.9
    # elif standard_deviation < 50:
    #     vrv_c = 0.4
    #     vrv_m = 0.85
    # elif standard_deviation < 100:
    #     vrv_c = 0.5
    #     vrv_m = 0.8
    # elif standard_deviation < 200:
    #     vrv_c = 0.6
    #     vrv_m = 0.5
    # elif standard_deviation < 300:
    #     vrv_c = 0.65
    #     vrv_m = 0.4
    # elif standard_deviation < 500:
    #     vrv_c = 0.85
    #     vrv_m = 0.2
    # else:
    #     vrv_c = 1
    #     vrv_m = 0.1

    while len(populacija) <= velicina_populacije:
        index1 = np.random.geometric(k, 1)[0] - 1
        index2 = np.random.geometric(k, 1)[0] - 1

        tree1 = df['funkcija'][index1].Kopija()
        tree2 = df['funkcija'][index2].Kopija()

        if rd.uniform(0, 1) <= vrv_c:
            if not crossover(tree1, tree2):
                continue

        if rd.uniform(0, 1) <= vrv_m:
            mutacija_parametri_normalna_raspodela(tree1)
            mutacija_parametri_normalna_raspodela(tree2)

        if rd.uniform(0, 1) <= vrv_m:
            mutacija_znakova(tree1)
            mutacija_znakova(tree2)

        if rd.uniform(0, 1) <= vrv_m:
            tree1 = mutacija_subdrvo_jedinka(tree1)
            tree2 = mutacija_subdrvo_jedinka(tree2)

        if rd.uniform(0, 1) <= vrv_m:
            tree1 = mutacija_randomizuj_subdrvo(tree1)
            tree2 = mutacija_randomizuj_subdrvo(tree2)

        niz_roditelja[index1] += 1
        niz_roditelja[index2] += 1

        if tree1.Depth() <= max_dubina:
            populacija.append(tree1.Kopija())
        if tree2.Depth() <= max_dubina:
            populacija.append(tree2.Kopija())


    il.plot_roditelje_xd(df, niz_roditelja, generacija)

    return populacija

def roulette_odabir(df, suma_fitnessa):
    r  = rd.uniform(0, suma_fitnessa) * 0.7
    rx = 0
    for index, rows in df.iterrows():
        fitness  = rows["fitness"]
        funkcija = rows["funkcija"]

        rx += max_odstupanje - fitness
        if rx >= r:
            return (funkcija.Kopija(), index)

    return df['funkcija'][-1].Kopija()

def izaberi_random_noud(tree, broj_koraka):
    if broj_koraka == 1:
        if rd.uniform(0, 1) <= 0.5:
            return [tree, 1]
        else:
            return [tree, 2]

    noud_1 = tree.F1().NodesBelow()
    noud_2 = tree.F2().NodesBelow()
    vrv1   = noud_1 / (noud_1 + noud_2+1)

    if rd.uniform(0, 1) <= vrv1:
        if type(tree.F1()) != type(klase.ComplexFunction(1, 1, 1)):
            return [tree, 1]
        else:
            return izaberi_random_noud(tree.F1(), broj_koraka - 1)
    else:
        if type(tree.F2()) != type(klase.ComplexFunction(1, 1, 1)):
            return [tree, 2]
        else:
            return izaberi_random_noud(tree.F2(), broj_koraka - 1)

def izaberi_random_broj_koraka(dubina):
    uk = dubina*(dubina+1)/2
    if 1 >= uk:
        return uk
    r  = rd.randint(1, uk)
    rx = 0
    for i in range(1, dubina+1):
        rx += i
        if rx >= r:
            return i
    return dubina

def mutacija_parametri_normalna_raspodela(tree):
    if type(tree) != type(klase.ComplexFunction(1,1,1)):
        if type(tree) == type(klase.Variable()):
            return

        if type(tree) == type(klase.Trygonometry("sin")):
            if rd.uniform(0, 1) <= sansa_promene_trigonometrije:
                sansa = rd.uniform(0, 1)
                if sansa <= 0.25:
                    tip = "sin"
                elif sansa <= 0.5:
                    tip = "cos"
                elif sansa <= 0.75:
                    tip = "tg"
                else:
                    tip = "ctg"

                tree.PromenaTipa(tip)
            return

        koef_promene = rd.normalvariate(nv_centar, nv_lambda)
        novi_koef    = tree.Param() + koef_promene
        tree.PromenaPara(novi_koef)

        return

    else:
        mutacija_parametri_normalna_raspodela(tree.F1())
        mutacija_parametri_normalna_raspodela(tree.F2())
        return

def mutacija_znakova(tree):
    if type(tree) != klase.ComplexFunction:
        return
    else:
        if rd.uniform(0, 1) <= vrv_operacija:
            tree.ChangeOp(er.generisi_random_op())
        mutacija_znakova(tree.F1())
        mutacija_znakova(tree.F2())

def mutacija_randomizuj_subdrvo(tree):
    if type(tree) != type(klase.ComplexFunction(1,1,1)):
        return tree
    broj_koraka = izaberi_random_broj_koraka(tree.Depth())
    noud_id     = izaberi_random_noud(tree, broj_koraka)

    random_drvo = er.grow_metoda(max_dubina - broj_koraka - 1)

    noud = noud_id[0]
    ide  = noud_id[1]

    if   ide == 1:
        noud.ChangeF1(random_drvo)
    elif ide == 2:
        noud.ChangeF2(random_drvo)

    tree.UpdateDepth()
    tree.UpdateNodesBelow()
    return tree

def mutacija_subdrvo_jedinka(tree):
    if type(tree) != type(klase.ComplexFunction(1,1,1)):
        return tree

    broj_koraka = int(rd.uniform(0, tree.Depth()))+1
    noud_id     = izaberi_random_noud(tree, broj_koraka)

    noud = noud_id[0]
    ide  = noud_id[1]

    tree.ChangeOp(noud.Op())
    tree.ChangeF1(noud.F1())
    tree.ChangeF2(noud.F2())

    tree.UpdateDepth()
    tree.UpdateNodesBelow()

    return tree

def crossover(root1, root2):

    if type(root1) != type(klase.ComplexFunction(1,1,1)) or type(root2) != type(klase.ComplexFunction(1,1,1)):
        return False
    d1 = root1.Depth()
    d2 = root2.Depth()

    if d1 < d2:
        pom   = root1
        root1 = root2
        root2 = pom
        d1    = root1.Depth()
        d2    = root2.Depth()

    br1  = int(rd.uniform(d1 - d2, root1.Depth()) + 1)
    br2  = int(rd.uniform(d2 - d1 + br1, d2) + 1)
    pom1 = izaberi_random_noud(root1, br1)
    pom2 = izaberi_random_noud(root2, br2)

    node1 = pom1[0]
    node2 = pom2[0]
    f1    = pom1[1]
    f2    = pom2[1]

    if   f1 == 1 and f2 == 1:
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
    return True

def trimmed_mean(fitness):
    pocetak = int(len(fitness) * 0.1)
    kraj    = int(len(fitness) * 0.9)
    suma    = sum([fitness[i] for i in range(pocetak, kraj+1)])
    return round(suma/(kraj+1-pocetak), 3)

def top_percent_average(fitness, percent):
    kraj = int(len(fitness)*percent)
    suma = sum([fitness[i] for i in range(0, kraj+1)])
    return round(suma/kraj, 3)

def rulet_odabir_rank(df, niz, suma):
    n = len(niz)
    a = rd.uniform(0, suma)
    ax = 0
    for i in range(n):
        ax += niz[i]
        if ax >= a:
            return df['funkcija'][i].Kopija(), i
    return df['funkcija'][n-1].Kopija(), n-1







