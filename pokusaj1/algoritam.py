import math
import pandas as pd
import numpy as np
import random
import klase
import funkcije as f

generacija = 1

konstanta = klase.Constant(4)
var = klase.Trygonometry("sin")
kompleksna = klase.ComplexFunction(konstanta, var, '*')

grafik = []
for x in range (-100, 100):
    grafik.append([x, kompleksna.getValue(x)])

populacija = f.inicijacija_populacije()

while generacija == 1 or najbolji_specimen >= 0:
    print("Generacija: " + str(generacija))
    fitness_podaci = f.izracunaj_fitness(populacija, grafik)
    f.izaberi_jednog_roditelja(fitness_podaci)
    break

