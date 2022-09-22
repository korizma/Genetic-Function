import math
import pandas as pd
import numpy as np
import random
import klase
import funkcije as f
import time
import mutacija_crossover as mc
import parametri
import expression_random as er
import sys
import os
import ispis_logova as il
import gc

gc.enable()

path = "C:\\Users\\Dušan\\Documents\\Petnica\\RAC2\\ActualProjekat2022\\2022\\logs\\"
generacija = 1
velicina_populacije = parametri.velicina_populacije()
max_dubina = parametri.max_dubina()
kriterijum_za_stajanje = parametri.kriterijum_za_stajanje()
procenat_top_jedinki = parametri.procenat_top_jedinki()
max_generacija = parametri.max_generacija()

kompleksna = er.grow_metoda(max_dubina)

grafik = []
for x in range (-100, 100):
    grafik.append([x, kompleksna.getValue(x)])

il.trazena_fja(kompleksna)                      # cuvamo funkciju i x tacke

populacija = f.populacija_half_half()

ostani = True

ftns = []

for i in populacija:
    fitness_i = f.fitness_povecavanje(i, grafik)
    ftns.append([i, fitness_i])


df = pd.DataFrame(ftns, columns=["func", "fitness"])
il.zapisi_jedinke_csv(df, generacija)
df = df.sort_values(by="fitness", ignore_index=True, ascending=True)

il.sacuvaj_top_10_klase(df, generacija)
il.plotuj_fitnese(df['fitness'], generacija)
il.prosecni_fitness(df['fitness'], generacija)

ostalo_nova_populacija = velicina_populacije

top_populacija = df.iloc[0:int(velicina_populacije * procenat_top_jedinki)]
ostalo_nova_populacija -= int(velicina_populacije * procenat_top_jedinki)

if top_populacija['fitness'][0] < kriterijum_za_stajanje:
    ostani = False
    best = top_populacija.iloc[0]

if ostani:
    wow_pop = mc.pravljenje_nove_generacije(df, ostalo_nova_populacija)
    populacija = wow_pop


while ostani and generacija < max_generacija:
    generacija += 1
    ftns = []

    for i in populacija:
        fitness_i = f.fitness_povecavanje(i, grafik)
        ftns.append([i, fitness_i])


    df = pd.DataFrame(ftns, columns=["func", "fitness"])
    df = pd.concat([df, top_populacija], axis=0)
    il.zapisi_jedinke_csv(df, generacija)
    df = df.sort_values(by="fitness", ignore_index=True, ascending=True)

    il.sacuvaj_top_10_klase(df, generacija)
    il.plotuj_fitnese(df['fitness'], generacija)
    il.prosecni_fitness(df['fitness'], generacija)

    ostalo_nova_populacija = velicina_populacije

    top_populacija = df.iloc[0:int(velicina_populacije * procenat_top_jedinki)]
    ostalo_nova_populacija -= int(velicina_populacije * procenat_top_jedinki)

    if top_populacija['fitness'][0] < kriterijum_za_stajanje:
        best = top_populacija.iloc[0]
        break


    wow_pop = mc.pravljenje_nove_generacije(df, ostalo_nova_populacija)
    populacija = wow_pop





