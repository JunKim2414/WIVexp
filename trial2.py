import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import math

class FileHandler:
    def __init__(self, dir):
        self.dir = dir
        self.parsing()
        self.getPower()

    def parsing(self):
        data = pd.read_csv(self.dir, sep = '\t')
        data = data.to_numpy()

        self.t = np.array(data[:,0])
        self.V = np.array(data[:,1])
        self.I = np.array(data[:,2])
        self.PM = np.array(data[:,3])
        self.DM = np.array(data[:,4])
        print('t length : {}'.format(len(self.t)))
        print(self.t)


    def getPower(self):
        ohm = 10000
        Vrms = math.sqrt(sum([i**2 for i in self.V])/len(self.V))
        self.power = Vrms**2/self.ohm

test = FileHandler('../wiv_raw_data/S-S5-W047/020.dat')



        # pd.read_csv(dir,\
        # names = ['t', 'v', 'I', 'p', 'd','tmp'],\
        # skiprows = 1, sep='\t', header = None)


'''
        folderDir = glob.glob(dir)
        # folderDir is a directory like "/Users/junkim/workspace/wiv_raw_data/C-S3-W130"
        for i in folderDir:
            testfolder = i.split('/')[-1]
            #testfolder is a folder like C-S5-W130.
            datfiles = i+'/*.dat'
            datdir = glob.glob(datfiles)
            # pprint(datdir) #'../wiv_raw_data/S-S5-W047/020.dat']

    def filter(self): #moving average
        pass


class PowerCalc():
    def getPower(self):
        sum = 0
        for i in data.v:
            sum = sum + i**2
        ohm = 10000
        Vrms = math.sqrt(sum)/len(self.v)
        power = Vrms**2 /ohm * 1000

    def errorbar(self):
        pass

    def powerPlot(self):
        pass


class FFT():
    def getFreq(self):
        pass

    def psd(self):
        pass







def powerCalc():

    sum = 0
    for i in data.v:
        sum = sum + i**2
    # other ways
    # a = data.v**2
    # b = a.sum()
    # print((data.v**2).sum())
    ohm = 10000
    length = len(data.v)
    Vrms = math.sqrt(sum)/length
    power = Vrms**2 / ohm * 10**3
    # print(f'{power:.8f}', dir) # mW


folderDir = glob.glob('../wiv_raw_data/*')
# folderDir is a directory like "/Users/junkim/workspace/wiv_raw_data/C-S3-W130"
for i in folderDir:
    testfolder = i.split('/')[-1]
    #testfolder is a folder like C-S5-W130.
    datfiles = i+'/*.dat'
    datdir = glob.glob(datfiles)
    # pprint(datdir) #'../wiv_raw_data/S-S5-W047/020.dat']
    for dir in datdir:
        V = [0.1,0.2,0.3,0.4,0.5,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0,1.1]
        tmpdata = pd.read_csv(dir,\
        names = ['t', 'v', 'I', 'p', 'd','tmp'],\
        skiprows = 1, sep='\t', header = None)
        data = tmpdata.drop(['tmp'], axis=1) #delete tmp column.
        powerCalc()
        plt.plot(V, power)
        plt.show()
        # pprint(dir)
        # pprint(data['v'])


'''
