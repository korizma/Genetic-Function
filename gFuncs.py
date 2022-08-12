import math
import pandas as pd
import numpy as np
import random
import klase

#parameters of random functions
max_const = 10
max_log_base = 10
max_exp_base = 10
max_nroot = 10
num_of_f_population = 10
num_of_f_specimen = 10


def createNFunctions(type, num_of_fs):
    global max_nroot, max_const, max_log_base, max_exp_base
    random.random()
    array = []
    for i in range(num_of_fs):
        if type == 'var':
            array.append(klase.Variable())
        elif type == 'log':
            array.append(klase.Logarithm(random.uniform(0, max_log_base)))
        elif type == 'exp':
            array.append(klase.Exponential(random.uniform(0, max_log_base)))
        elif type == 'nroot':
            array.append(klase.NRoot(random.randint(1, max_nroot), klase.Variable()))
        elif type == "cos" or type == "sin" or type == "tg" or type == "ctg":
            array.append(klase.Trygonometry(type))
        else:
            array.append("not a function")
    return array

def fitness(graph, f):
    score = 0
    undefined = 0
    for dot in graph:
        x = dot[0]
        y = dot[1]
        if f.getValue(x) == "Undefined":
            undefined += 1
        else:
            y_delta = abs(y - f.getValue(x))
            score += y_delta
    if len(graph) == undefined:
        return [1000000, 0]
    return [round(score / (len(graph) - undefined), 3), undefined]

def mutation(f1, f2):
    array = []
    array.append(klase.ComplexFunction(f1, f2, '+'))
    array.append(klase.ComplexFunction(f1, f2, '-'))
    array.append(klase.ComplexFunction(f1, f2, '*'))
    array.append(klase.ComplexFunction(f1, f2, '/'))
    array.append(klase.ComplexFunction(f1, f2, 'o'))
    return array

def mutate_population(population):
    mutated = []

    for f in population:
        for g in population:
            mutated += mutation(f, g)

    return mutated


def create_population():
    global num_of_f_population
    population = []

    population += createNFunctions("var", 1)
    population += createNFunctions("log", num_of_f_population)
    population += createNFunctions("exp", num_of_f_population)
    population += createNFunctions("nroot", num_of_f_population)
    population += createNFunctions("cos", 1)
    population += createNFunctions("sin", 1)
    population += createNFunctions("tg", 1)
    population += createNFunctions("ctg", 1)

    return population

def create_specimen():
    global num_of_f_specimen

    specimen = []
    specimen += createNFunctions("log", num_of_f_specimen)
    specimen += createNFunctions("exp", num_of_f_specimen)
    specimen += createNFunctions("nroot", num_of_f_specimen)

    return specimen

def create_const():
    constants = []

    for num in range(1, max_const):
        constants += klase.Constant(random.uniform(num, num + 1))
        constants += klase.Constant(random.uniform(-num, 1 - num))
    constants += klase.Constant(random.uniform(0, 1))

    return constants

def evolve_specimen(f, graph):
    s = fitness(graph, f)
    new_fs = []

    new_fs.append([f] + s)
    s = klase.Constant(s[0])

    new_f = klase.ComplexFunction(f, s, "+")
    new_fs.append([new_f] + fitness(graph, new_f))

    new_f = klase.ComplexFunction(f, s, "-")
    new_fs.append([new_f] + fitness(graph, new_f))

    pom = klase.Constant(-1)
    new_f = klase.ComplexFunction(f, pom, '*')
    new_fs.append([new_f] + fitness(graph, new_f))

    pom = klase.Constant(1)
    new_f = klase.ComplexFunction(pom, f, '/')
    new_fs.append([new_f] + fitness(graph, new_f))

    pom = klase.Constant(-1)
    new_f = klase.ComplexFunction(pom, f, '/')
    new_fs.append([new_f] + fitness(graph, new_f))

    return new_fs