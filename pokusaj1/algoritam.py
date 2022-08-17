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

generacija = 1
velicina_populacije = parametri.velicina_populacije()
max_dubina = parametri.max_dubina()

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
    fitness_i = f.fitness_odstupanje(i, grafik)
    ftns.append([i, fitness_i])
print("fitnes izracunat za: " + str(time.time() - start) + "s")

df = pd.DataFrame(ftns, columns=["func", "fitness"])
df = df.sort_values(by="fitness", ignore_index=True, ascending=True)
suma = sum(i for i in df['fitness'])
print()
print("prosecan fitness: " + str(round(suma/len(df['fitness']), 3)))
print()
print("zavrsen fitness i sortirano")

print("kreiranje nove popoulacije")

ostalo_nova_populacija = velicina_populacije

top_populacija = df.iloc[0:int(velicina_populacije*0.1)]
ostalo_nova_populacija -= int(velicina_populacije*0.1)

if top_populacija['fitness'][0] < 0.01:
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
    max_depth = 0
    for i in populacija:
        fitness_i = f.fitness_odstupanje(i, grafik)
        ftns.append([i, fitness_i])

    print("fitnes izracunat za: " + str(time.time() - start) + "s")
    df = pd.DataFrame(ftns, columns=["func", "fitness"])
    df = pd.concat([df, top_populacija], axis=0)
    df = df.sort_values(by="fitness", ignore_index=True, ascending=True)

    suma = sum(i for i in df['fitness'])
    print()
    print("prosecan fitness: " + str(round(suma/len(df['fitness']), 3)))
    print()
    print("zavrsen fitness i sortirano")

    print("kreiranje nove popoulacije")


    ostalo_nova_populacija = velicina_populacije

    top_populacija = df.iloc[0:int(velicina_populacije*0.1)]
    ostalo_nova_populacija -= int(velicina_populacije*0.1)

    if top_populacija['fitness'][0] < 0.01:
        best = top_populacija.iloc[0]
        break

    print("///")
    print(top_populacija['func'][0].ViewF())
    print("fitness: " + str(top_populacija['fitness'][0]))
    print("///")

    wow_pop = mc.rulet_mutacija_crossover(df, ostalo_nova_populacija)
    populacija = wow_pop

    print("kraj generacije " + str(generacija-1))
    print()
    print("/////////////////////////////////////////////////////////////////////////////////////")
    print()


print(best['func'].ViewF())
print(best['fitness'])
print(kompleksna.ViewF())


