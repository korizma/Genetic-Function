import math
import pandas as pd
import numpy as np
import random
import klase
import gFuncs as gf

number_of_top_specimen = 100
gen = 0

#making an example graph
#graph contains the coordinates of the function 4*x

konstanta = klase.Constant(4)
var = klase.Variable()
kompleksna = klase.ComplexFunction(konstanta, var, '*')

graph = []
for x in range (-100, 100):
    graph.append([x, kompleksna.getValue(x)])


#creating a population
population = gf.create_population()

#we are getting the results from the fitness function
#in the array every row looks like this: [FUNCTION, SCORE, UNDEFINED]
#SCORE represents the average distance between the dots of the original graph and the dots of the graphe defined by our given function
#UNDEFINED represents the number of undefined dots our function has when compared to the original graph
p_fitness = []
for f in population:
    p_fitness += gf.evolve_specimen(f, graph)

#sorting the fitness results, but first we have to turn our 2D array into a pandas DataFrame
p_fitness = pd.DataFrame(p_fitness, columns=["function", "score", "undefined"])
p_fitness = p_fitness.sort_values(by="score", ascending=True, ignore_index=True)

#getting the best fitted functions
top_specimen = p_fitness[:number_of_top_specimen]

#finding the best specimen that has no UNKNOWN value
best_specimen = top_specimen.iloc[0]
for i in range(0, number_of_top_specimen):
    k = top_specimen.iloc[i]
    if k[2] == 0:
        best_specimen = k
        break

while best_specimen[1] > 1 :
    print(gen)
    print(best_specimen[0].ViewF())
    print(best_specimen)
    gen += 1
    #create new specimen, because of unchangeable functions like log exp and nroot
    #we have to keep updating them so we always have the best specimen available for mutation
    new_specimen = gf.create_specimen()
    pom = []
    for f in new_specimen:
        pom += gf.evolve_specimen(f, graph)

    pom = pd.DataFrame(pom, columns=["function", "score", "undefined"])
    top_specimen = pd.concat([top_specimen, pom], ignore_index=True)

    top_specimen = top_specimen.sort_values(by="score", ascending=True, ignore_index=True)
    top_specimen = top_specimen[:number_of_top_specimen]

    population = top_specimen["function"]

    new_population = gf.mutate_population(population)

    np_fitness = []
    for f in new_population:
        np_fitness += gf.evolve_specimen(f, graph)

    np_fitness = pd.DataFrame(np_fitness, columns=["function", "score", "undefined"])

    all_fitness = pd.concat([top_specimen, np_fitness], ignore_index=True)
    all_fitness = all_fitness.sort_values(by="score", ascending=True, ignore_index=True)

    top_specimen = all_fitness[:number_of_top_specimen]

    best_specimen = top_specimen.iloc[0]
    for i in range(0, 100):
        k = top_specimen.iloc[i]
        if k[2] == 0:
            best_specimen = k
            break

    print(best_specimen[0].ViewF())
    print(best_specimen)