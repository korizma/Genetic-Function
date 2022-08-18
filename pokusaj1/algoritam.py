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

path = "C:\\Users\\Dušan\\Documents\\Petnica\\RAC2\\ActualProjekat2022\\2022\\logs\\"
generacija = 1
velicina_populacije = parametri.velicina_populacije()
max_dubina = parametri.max_dubina()
kriterijum_za_stajanje = parametri.kriterijum_za_stajanje()
procenat_top_jedinki = parametri.procenat_top_jedinki()
ime = len(os.listdir(path))+1

kompleksna = er.grow_metoda(max_dubina)

grafik = []
for x in range (-100, 100):
    grafik.append([x, kompleksna.getValue(x)])

# kreiranje populacije
start = time.time()

populacija = f.populacija_half_half()

end = time.time()
print("kreiranje populacije je trajalo: " + str(end - start))

ostani = True

print("generacija: " + str(generacija))
generacija += 1
ftns = []
start = time.time()

for i in populacija:
    pork = [i.ViewF()]
    il.log(pork, str(ime))

    fitness_i = f.fitness_odstupanje(i, grafik)
    ftns.append([i, fitness_i])

print("fitnes izracunat za: " + str(time.time() - start) + "s")

df = pd.DataFrame(ftns, columns=["func", "fitness"])
df = df.sort_values(by="fitness", ignore_index=True, ascending=True)

# <editor-fold desc="print shit">
suma = sum(i for i in df['fitness'])
print()
print("prosecan fitness: " + str(round(suma/len(df['fitness']), 3)))
print()
print("zavrsen fitness i sortirano")

print("kreiranje nove popoulacije")
# </editor-fold>

ostalo_nova_populacija = velicina_populacije

top_populacija = df.iloc[0:int(velicina_populacije * procenat_top_jedinki)]
ostalo_nova_populacija -= int(velicina_populacije * procenat_top_jedinki)

if top_populacija['fitness'][0] < kriterijum_za_stajanje:
    ostani = False
    best = top_populacija.iloc[0]

if ostani:
    wow_pop = mc.rulet_mutacija_crossover(df, ostalo_nova_populacija)
    populacija = wow_pop

print("kraj generacije " + str(generacija - 1))

while ostani:
    print("generacija " + str(generacija) + " trenutno se racuna fitness")
    generacija += 1
    ftns = []
    start = time.time()

    for i in populacija:
        pork = [i.ViewF(), str(i.Depth())]
        il.log(pork, str(ime))

        fitness_i = f.fitness_odstupanje(i, grafik)
        ftns.append([i, fitness_i])

    print("fitnes izracunat za: " + str(time.time() - start) + "s")

    df = pd.DataFrame(ftns, columns=["func", "fitness"])
    df = pd.concat([df, top_populacija], axis=0)
    df = df.sort_values(by="fitness", ignore_index=True, ascending=True)

    # <editor-fold desc="print shit">
    suma = sum(i for i in df['fitness'])
    print()
    print("prosecan fitness: " + str(round(suma/len(df['fitness']), 3)))
    print()
    print("zavrsen fitness i sortirano")

    print("kreiranje nove popoulacije")
    # </editor-fold>


    ostalo_nova_populacija = velicina_populacije

    top_populacija = df.iloc[0:int(velicina_populacije * procenat_top_jedinki)]
    ostalo_nova_populacija -= int(velicina_populacije * procenat_top_jedinki)

    if top_populacija['fitness'][0] < kriterijum_za_stajanje:
        best = top_populacija.iloc[0]
        break

    # <editor-fold desc="print shit">
    print("///")
    print(top_populacija['func'][0].ViewF())
    print("fitness: " + str(top_populacija['fitness'][0]))
    print("///")
    # </editor-fold>

    wow_pop = mc.rulet_mutacija_crossover(df, ostalo_nova_populacija)
    populacija = wow_pop

    # <editor-fold desc="print shit">
    print("kraj generacije " + str(generacija-1))
    print()
    print("/////////////////////////////////////////////////////////////////////////////////////")
    print()
    # </editor-fold>


print(best['func'].ViewF())
print(best['fitness'])
print(kompleksna.ViewF())


