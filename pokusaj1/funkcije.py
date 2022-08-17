import math
import pandas as pd
import numpy as np
import random
import klase
import numpy.random as npr
import expression_random as er
import parametri

#parametri
velicina_populacije = parametri.velicina_populacije()
max_dubina = parametri.max_dubina()

povecanje = parametri.povecanje()
na_koliko_tacaka = parametri.na_koliko_tacaka()

donja_granica = -25
gornja_granica = 25        #granice za random brojeve

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

max_odstupanje = parametri.max_odstupanje()

def fitness_odstupanje(funkcija, grafik):
    global max_odstupanje
    skor = 0

    for tacka in grafik:
        x = tacka[0]
        y = tacka[1]
        dy = funkcija.getValue(x)
        if math.isnan(y) and math.isnan(dy):
            odstupanje = 0
        elif math.isnan(y) and not math.isnan(dy):
            odstupanje = max_odstupanje
        else:
            odstupanje = abs(dy - y)

            if math.isnan(dy) or odstupanje > max_odstupanje:
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
        if math.isnan(dy):
            br_nana += 1
        else:
            skor += abs(dy - y) ** 2

    skor = math.sqrt(skor / (len(grafik)-br_nana))
    for i in (0, br_nana, na_koliko_tacaka):
        skor *= povecanje
    return skor


def populacija_half_half():
    global velicina_populacije, max_dubina
    populacija = []

    grow = int((velicina_populacije/5)*4)
    full = velicina_populacije - grow
    for i in range(0, grow):
        populacija.append(er.grow_metoda(max_dubina))
    for i in range(0, full):
        populacija.append(er.full_metoda(random.randint(1, max_dubina)))

    return populacija










