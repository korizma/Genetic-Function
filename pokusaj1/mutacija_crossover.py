import math
import pandas as pd
import numpy as np
import random as rd
import klase
import expression_random as er
import copy


def mutacija_rnd_tree(root, broj_koraka, max_depth_rnd_drveta):
    vf1 = root.F1().Depth() + 1
    vf2 = root.F2().Depth() + 1
    vrv = vf1 /(vf1+vf2)

    rnd_br = rd.uniform(0,1)

    if broj_koraka == 1:
        if rnd_br < vrv:
            root.ChangeF1(er.grow_metoda(max_depth_rnd_drveta))             #ovde ide random f_ja
            return
        else:
            root.ChangeF2(er.grow_metoda(max_depth_rnd_drveta))             #ovde ide random f_ja
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


drvo_pocetak = er.grow_metoda(10)
drvo_mutacija = copy.deepcopy(drvo_pocetak)
mutacija_rnd_tree(drvo_mutacija, rd.randint(1,drvo_pocetak.Depth()), drvo_pocetak.Depth())
drvo_mutacija.UpdateDepth()
print(drvo_pocetak.ViewF())
print(drvo_mutacija.ViewF())




