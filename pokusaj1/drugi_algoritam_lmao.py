import math
import pandas as pd
import numpy as np
import random
import klase
import funkcije as f
import time
import nova_mc as mc
import parametri
import expression_random as er
import sys
import os
import ispis_logova1 as il
import gc

gc.enable()

# <editor-fold desc="Parametri">
generacija = 0
velicina_populacije = parametri.velicina_populacije()
max_dubina = parametri.max_dubina()
kriterijum_za_stajanje = parametri.kriterijum_za_stajanje()
procenat_top_jedinki = parametri.procenat_top_jedinki()
max_generacija = parametri.max_generacija()
# </editor-fold>

# <editor-fold desc="kreiranje trazene f-je i cuvanje grafika">
broj_nedefinisanih = 0
n = 0
funkcija_trazena = er.grow_metoda(max_dubina)
grafik = []
x = -100
while x <= 100:
    p = funkcija_trazena.getValue(x)
    grafik.append([x, p])
    if math.isnan(p):
        broj_nedefinisanih += 1
    x += 0.5
    n += 1

il.trazena_fja(funkcija_trazena)                      # cuvamo funkciju i x tacke
# </editor-fold>

populacija = f.populacija_half_half()
ostani = True

while ostani and max_generacija >= generacija:
    generacija += 1

    fitness_populacije = []

    for funkcija in populacija:
        if funkcija.Depth() == 0:
            funkcija.UpdateDepth()
        fitness_funkcije = f.fitness_odstupanje(funkcija, grafik)
        fitness_populacije.append(fitness_funkcije)

    populacija = pd.DataFrame(populacija, columns=["funkcija"])
    fitness_populacije = pd.DataFrame(fitness_populacije, columns=["fitness"])
    df = pd.concat([populacija, fitness_populacije], axis=1)


    df = df.sort_values(by="fitness", ignore_index=True, ascending=True)

    il.sacuvaj_top_10_klase(df, generacija)
    il.plotuj_fitnese(df['fitness'], generacija)
    il.zapisi_jedinke_csv(df, generacija)
    il.zapisi_sve_csv(df, generacija)

    if df["fitness"][0] < kriterijum_za_stajanje or max_generacija == generacija:
        break

    populacija = mc.totalno_nova_generacija(df, generacija)

for i in range(10):
    il.log("fitness " + str(i) + "-te na kraju je: " + str(il.poredjenje_trazene_jedinki(funkcija_trazena, df['funkcija'][i])), "fitness_van_tacaka")
il.log("Nedefinisanih tacaka je bilo " + str(broj_nedefinisanih) + " od " + str(n) + " tacaka", "nedefinisane")
x = -100
korak = 0.5
for i in range(10):
    fned = 0
    while x <= -100:
        if math.isnan(df['funkcija'][i].getValue(x)):
            fned += 1
        x += korak
    il.log("Nedefinisanih tacaka je bilo " + str(broj_nedefinisanih) + " od " + str(n) + " tacaka za funkciju na mestu " + str(i+1), "nedefinisane")


