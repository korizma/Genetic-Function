import time
import datetime
import os, os.path

path = "C:\\Users\\Dušan\\Documents\\Petnica\\RAC2\\ActualProjekat2022\\2022\\logs\\"

def log(poruke, ime):
    global path
    file = open(path + ime + ".log", 'a')

    for i in poruke:
        file.write(i)
        file.write('\n')


