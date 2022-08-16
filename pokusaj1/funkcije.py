import math
import pandas as pd
import numpy as np
import random
import klase
import numpy.random as npr
import expression_random as er

#parametri
broj_funkcija = 10      #4 razlicitih tipova (40), 4 trigonometrijske i jedna promenljiva = 45 u populaciji
donja_granica = -25
gornja_granica = 25        #granice za random brojeve
broj_specimena_koje_cuvamo = 10

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def random_broj():
    global donja_granica, gornja_granica
    return random.uniform(donja_granica, gornja_granica)

max_odstupanje = 500

def fitness_odstupanje(funkcija, grafik):
    global max_odstupanje
    skor = 0

    for tacka in grafik:
        x = tacka[0]
        y = tacka[1]
        dy = funkcija.getValue(x)
        if math.isnan(y) and math.isnan(dy):
            odstupanje = 0
        else:
            odstupanje = abs(dy - y)

            if math.isnan(dy) or odstupanje > max_odstupanje:
                odstupanje = max_odstupanje

        skor += odstupanje ** 2

    skor = math.sqrt(skor / len(grafik))
    return skor

povecanje = 2
na_koliko_tacaka = 5

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

velicina_populacije = 10
max_dubina = 10

def populacija_half_half():
    global velicina_populacije, max_dubina
    populacija = []

    grow = int(velicina_populacije/2)
    full = velicina_populacije - grow
    for i in range(0, grow):
        populacija.append(er.grow_metoda(max_dubina))
    for i in range(0, full):
        populacija.append(er.full_metoda(random.randint(1, max_dubina)))

    return populacija










