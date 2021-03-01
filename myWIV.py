import glob
import math
from pprint import pprint
import matplotlib.pyplot as plt

class PowerCalc():
    def __init__(self, fileDirectory):
        self.ohm = 10000
        self.t = []
        self.V = []
        self.I = []
        self.Angle = []
        self.dynamo = []
        self.power = None
        self.parse(fileDirectory)
        self.powering()

    def parse(self, fileDirectory):
        f = open(fileDirectory)
        tmp = f.readlines()

        for row in tmp[1::]:
            splited = row.split()
            self.t.append(float(splited[0]))
            if abs(float(splited[1]))>100:   #노이즈로 튄 값을 제거
                self.V.append(0)
            else:
                self.V.append(float(splited[1]))
            #self.V.append(float(splited[1]))

            self.I.append(float(splited[2]))
            self.Angle.append(float(splited[3]))
            self.dynamo.append(float(splited[4]))

    def powering(self):
        Vrms = math.sqrt(sum([i**2 for i in self.V])/len(self.V))
        self.power = Vrms**2/self.ohm

class project():
    V = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1]
    def __init__(self, testcaselist):
        self.resultDict = {}
        for case in testcaselist:
            Name = case.split('/')[-1]
            tmpfile= case+'/*.dat'
            fileList = glob.glob(tmpfile)
            tmpExpList=[]
            for file in fileList:
                if 'initial' in file:
                    pass
                else:
                    tmpExpList.append(PowerCalc(file))
            self.resultDict[Name]=tmpExpList
    def report(self):
        for caseName in self.resultDict:
            expList = self.resultDict[caseName]
            powerlist = [i.power for i in expList]
            try:
                #plt.plot(project.V,powerlist,'ro:')
                plt.plot(project.V,powerlist,'o-',markersize=0.8,lw=1)
                #plt.title(caseName)
                #plt.show()
            except:
                V = [0.1,0.2,0.3,0.4,0.5,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0,1.1]
                #plt.plot(V,powerlist,'bo:')
                plt.plot(V,powerlist)
                #plt.title(caseName)
                #plt.show()

        plt.legend(self.resultDict.keys())

if __name__ =='__main__':
    testcaselist = glob.glob('../wiv_raw_data/*')
    proj = project(testcaselist)
    proj.report()
    plt.show()



# pprint(glob('C:/Users/Jun/Desktop/WIV_EXP/wiv_raw_data/C-S3-W130/???.dat'))
'''
f = open('C:/Users/Jun/Desktop/WIV_EXP/wiv_raw_data/C-S3-W130/010.dat')
lines = f.readlines()
for row in lines[1::]:
    splited = row.split()
pprint(type(float(splited[0])))
'''
