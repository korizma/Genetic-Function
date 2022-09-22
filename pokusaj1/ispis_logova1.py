import os, os.path
import klase
import pandas as pd
import matplotlib.pyplot as plt
import math
import parametri
import pandas as pd

path = "C:\\Users\\Dušan\\Documents\\Petnica\\RAC2\\ActualProjekat2022\\2022\\logs\\2.13\\"
# path = "C:\\Users\\Korizma\\Documents\\SVA INFORMATIKA NAJVEROVATINJE\\petnica\\RAC2\\ActualActualProjekt2022\\logs\\2.5\\"

max_odstupanje = parametri.max_odstupanje()

def log(poruke, ime):
    global path
    file = open(path + ime + ".log", 'a')

    file.write(str(poruke))
    file.close()

def plotuj_fitnese(fitness, generacija):
    ceo_path = path + "fitness\\" + str(generacija) + "_plot_fitnessa.jpg"
    plt.clf()
    plot = fitness.plot()
    fig = plot.get_figure()
    fig.savefig(ceo_path)

def sacuvaj_top_10_klase(df, generacija):
    ceo_path = path + "top jedinke\\" + str(generacija) + "_top_10_generacije.csv"
    df = df.iloc[0:10]
    novi_df = []
    for index, row in df.iterrows():
        func = row['funkcija']
        fit = row['fitness']
        depth = func.Depth()
        novi_df.append([func.ViewF(), fit, depth, index])
    novi_df = pd.DataFrame(novi_df, columns=["funkcija", "fitness", "depth", "pozicija"])
    novi_df.to_csv(ceo_path)

def plotuj_funkciju(funk, ime_slike):
    grafik = []
    for i in range(1000):
        x = -100 + (0.2 * i)
        y = funk.getValue(x)
        grafik.append([x, y])
    grafik = pd.DataFrame(grafik, columns=["x", "y"])
    plot = grafik.plot(x="x", y="y", title=funk.ViewF())
    fig = plot.get_figure()
    fig.set_figwidth(20)
    fig.set_figheight(8)
    fig.savefig(ime_slike)
    plt.clf()
    plt.close('all')

def trazena_fja(func):
    f = func.ViewF()
    file = open(path + "funkcija.txt", 'w')
    file.write(f + '\n')
    file.write("tacke su od -100 do 100")
    file.close()
    plotuj_funkciju(func, path + "trazena_fja.jpg")

def prosecni_fitness(fitness, generacija):
    suma = sum(i for i in fitness)
    prosek = round(suma/len(fitness), 3)
    ceo_path = path + str(generacija) + "_prosecni_fitness.txt"
    file = open(ceo_path, 'w')
    file.write("prosek je: " + str(prosek))
    file.close()

def zapisi_jedinke_csv(df, generacija):
    plotuj_funkciju(df['funkcija'][0], path +"prve\\" + str(generacija) + "_prva_jedinka.jpg")
    plotuj_funkciju(df['funkcija'][99], path + "stote\\" +str(generacija) + "_stota_jedinka.jpg")
    plotuj_funkciju(df['funkcija'][499], path + "petsto\\" +str(generacija) + "_petstota_jedinka.jpg")
    log("fitness prve u " + str(generacija) + ". generaciji je: " + str(df['fitness'][0]) + '\n', "fitnessi znacanijih")
    log("fitness stote u " + str(generacija) + ". generaciji je: " + str(df['fitness'][99]) + '\n', "fitnessi znacanijih")
    log("fitness pestote u " + str(generacija) + ". generaciji je: " + str(df['fitness'][499]) + '\n', "fitnessi znacanijih")

def zapisi_sve_csv(df, generacija):
    ceo_path = path + "sve jedinke generacije\\" +str(generacija) + "_generacija_cela.csv"

    novi_df = []
    for index, row in df.iterrows():
        func = row['funkcija']
        fit = row['fitness']
        depth = func.Depth()
        novi_df.append([func.ViewF(), fit, depth])
    novi_df = pd.DataFrame(novi_df, columns=["funkcija", "fitness", "depth"])
    novi_df.to_csv(ceo_path)

def zapisi_posle_cm(populacija, generacija):
    file = open(path + str(generacija) + "_populacija.log", 'w')
    for func in populacija:
        file.write(func.ViewF() + '\n')
    file.close()

def plot_roditelje_xd(df, niz_roditelja, generacija):
    n = len(niz_roditelja)

    ndf = []
    for index in range(n):
        if niz_roditelja[index] != 0:
            ndf.append([df['funkcija'][index].ViewF(), niz_roditelja[index], index])

    ndf = pd.DataFrame(ndf, columns=["roditelji", "broj_dece", "pozicija"])
    ndf.to_csv(path + "roditelji\\" + str(generacija) + "_roditelji.csv")


