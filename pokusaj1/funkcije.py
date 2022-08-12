import math
import pandas as pd
import numpy as np
import random
import klase
import numpy.random as npr

#parametri
broj_funkcija = 10      #4 razlicitih tipova (40), 4 trigonometrijske i jedna promenljiva = 45 u populaciji
donja_granica = -25
gornja_granica = 25        #granice za random brojeve
broj_specimena_koje_cuvamo = 10

def random_broj():
    global donja_granica, gornja_granica
    return random.uniform(donja_granica, gornja_granica)

def napravi_n_funkcija(broj, vrsta):
    funkcije = []
    for i in range(broj):
        if vrsta == "konst":
            funkcije.append(klase.Constant(random_broj()))
        elif vrsta == "nkoren":
            funkcije.append(klase.NRoot(random_broj()))
        elif vrsta == "log":
            funkcije.append(klase.Logarithm(random_broj()))
        elif vrsta == "eksp":
            funkcije.append(klase.Exponential( random_broj() ))
    return np.array(funkcije)

def inicijacija_populacije():
    global broj_funkcija

    funkcije = np.array([])

    funkcije = np.concatenate((funkcije, napravi_n_funkcija(broj_funkcija, "konst")), axis=0)
    funkcije = np.concatenate((funkcije, napravi_n_funkcija(broj_funkcija, "nkoren")), axis=0)
    funkcije = np.concatenate((funkcije, napravi_n_funkcija(broj_funkcija, "log")), axis=0)
    funkcije = np.concatenate((funkcije, napravi_n_funkcija(broj_funkcija, "eksp")), axis=0)

    funkcije = np.append(funkcije, klase.Variable())
    funkcije = np.append(funkcije, klase.Trygonometry("sin"))
    funkcije = np.append(funkcije, klase.Trygonometry("cos"))
    funkcije = np.append(funkcije, klase.Trygonometry("tg"))
    funkcije = np.append(funkcije, klase.Trygonometry("ctg"))

    return funkcije

def fitness(funkcija, grafik):
    skor = 0
    undefined = 0
    for tacka in grafik:
        x = tacka[0]
        y = tacka[1]
        if funkcija.getValue(x) == "Undefined":
            undefined += 1
        else:
            y_delta = abs(y - funkcija.getValue(x))
            skor += y_delta
    if len(grafik) == undefined:
        return [1000000, 0]
    return [round(skor / (len(grafik) - undefined), 3), undefined]

#podaci ce biti u formatu [FUNCTION, [SCORE, UNDEFINED]]

def izracunaj_fitness(populacija, grafik):
    fitness_rezultati = []
    for funkcija in populacija:
        fitness_rezultati.append([funkcija] + fitness(funkcija, grafik))
    return pd.DataFrame(fitness_rezultati, columns=["Funkcija", "Skor", "Undefined"])

def vrati_najbolje_specimene(fitness_podaci):
    global broj_specimena_koje_cuvamo
    fitness_podaci1 = fitness_podaci.sort_values(by="Skor", ascending=True, ignore_index=True)
    return fitness_podaci1.iloc[0:broj_specimena_koje_cuvamo]

def izaberi_jednog_roditelja(fitness_podaci):
    fitness = fitness_podaci.sort_values(by="Skor", ascending=True, ignore_index=True)
    max = fitness.iloc[-1]["Skor"]

    skorovi = [max-x for x in fitness["Skor"]]
    suma = sum(x for x in skorovi)
    verovatnoce = [x / suma for x in skorovi]
    print(skorovi)
    print(verovatnoce)
    if (verovatnoce[0] < verovatnoce[1]):
        print("noooooo")
    return



    max = sum([c.fitness for c in populacija])
    selection_probs = [c.fitness/max for c in populacija]
    return population[npr.choice(len(populacija), p=selection_probs)]

def mutacija(f1, f2):
    operacija = random.randint(0,4)
    if operacija == 0:
        return klase.ComplexFunction(f1, f1, "+")
    elif operacija == 1:
        return klase.ComplexFunction(f1, f1, "-")
    elif operacija == 2:
        return klase.ComplexFunction(f1, f1, "*")
    elif operacija == 3:
        return klase.ComplexFunction(f1, f1, "/")
    elif operacija == 4:
        return klase.ComplexFunction(f1, f1, "o")
    """
    elif operacija == 5:
        return komplikovana_mutacija(f1, f2)
"""
















