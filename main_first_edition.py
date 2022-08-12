import math
import pandas as pd
import numpy as np
import random
import klase
import gFuncs as gf

konstanta = klase.Constant(4)
var = klase.Variable()
kompleksna = klase.ComplexFunction(konstanta, var, '*')
graph = []
for x in range (-100, 100):
    graph.append([x, kompleksna.getValue(x)])

population = gf.create_population()
parents = []

while 1:
    population_fitness = []
    for f in population:
        population_fitness.append(gf.fitness(graph, f) + [f])

    population_fitness = pd.DataFrame(population_fitness, columns=['score', 'undefined', 'function'])
    population_fitness = population_fitness.sort_values(by='score', ascending=True, ignore_index=True)

    parents1 = population_fitness[:100]
    for index, row in parents1.iterrows():
        if float(row['score']) <= 2 and int(row['undefined']) != 0:
            print(row['function'].ViewF())
            break
    past_parents = parents
    parents = population_fitness['function'][:100]
    print(parents[0].ViewF())
    constants_helper = gf.createNFunctions('const', 100)
    population = []
    for f in parents:
        for g in parents:
            population += gf.mutation(f, g)
        for con in constants_helper:
            population += gf.mutation(f, con)
    for f in past_parents:
        for con in constants_helper:
            population += gf.mutation(f, con)




