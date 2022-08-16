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
for x in range (-1000, 1000):
    grafik.append([x, kompleksna.getValue(x)])

populacija = f.populacija_half_half()

for i in populacija:
        print(i.ViewF())


