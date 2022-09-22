import math
import pandas as pd
import numpy as np
import random
import klase
import numpy.random as npr
import expression_random as er
import parametri

# <editor-fold desc="Parametri">
#parametri
velicina_populacije = parametri.velicina_populacije()
max_dubina = parametri.max_dubina()

posto_grow_populacije = parametri.posto_grow_populacije()

povecanje = parametri.povecanje()
na_koliko_tacaka = parametri.na_koliko_tacaka()


max_odstupanje = parametri.max_odstupanje()

donja_granica = -25
gornja_granica = 25        #granice za random brojeve
# </editor-fold>

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def random_broj():
    global donja_granica, gornja_granica
    r = random.uniform(donja_granica, gornja_granica)
    if r < 0 and r > -1:
        return r - 1
    if r > 0 and r < 1:
        return r + 1
    return r

def fitness_odstupanje(funkcija, grafik):
    global max_odstupanje
    skor = 0

    for tacka in grafik:
        x = tacka[0]
        y = tacka[1]
        dy = funkcija.getValue(x)

        odstupanje = abs(dy - y)

        if math.isnan(y) and math.isnan(dy):
            odstupanje = 0

        elif math.isnan(y) and not math.isnan(dy):
            odstupanje = max_odstupanje

        elif math.isnan(dy) or odstupanje > max_odstupanje:
            odstupanje = max_odstupanje

        skor += odstupanje ** 2

    skor = math.sqrt(skor / len(grafik))
    return skor

# ovo nije gotovo
def fitness_povecavanje(funkcija, grafik):
    global povecanje, na_koliko_tacaka

    skor = 0
    br_nana = 0

    for tacka in grafik:
        x = tacka[0]
        y = tacka[1]
        dy = funkcija.getValue(x)
        if math.isnan(dy) and math.isnan(y):
            skor += 0
        elif (math.isnan(dy) and not math.isnan(y)) or (not math.isnan(dy) and math.isnan(y)):
            br_nana += 1
        else:
            skor += abs(dy - y) ** 2

    skor = math.sqrt(skor / (len(grafik)-br_nana))
    if skor == 0 and br_nana != 0:
        skor = 1000000
        return skor
    for i in (0, br_nana, na_koliko_tacaka):
        skor *= povecanje
    return skor

def populacija_half_half():
    global velicina_populacije, max_dubina, posto_grow_populacije
    populacija = []

    grow = int(velicina_populacije*posto_grow_populacije)
    full = velicina_populacije - grow
    for i in range(0, grow):
        f = er.grow_metoda(max_dubina)
        populacija.append(f)

        f.UpdateDepth()
        f.UpdateNodesBelow()

    for i in range(0, full):
        f = er.full_metoda(random.randint(1, max_dubina))
        populacija.append(f)

        f.UpdateDepth()
        f.UpdateNodesBelow()

    return populacija


def klemp(vrednost, manje, vece):
    if vrednost <= manje or vrednost >= vece:
        return float('NaN')
    return vrednost







