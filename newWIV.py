import glob
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
import math


#def parse():
folderDir = glob.glob('../wiv_raw_data/*')
for tmp in folderDir:
    testcaselist = tmp.split('/')[-1]
    datfiles = tmp+'/*.dat'
    real = glob.glob(datfiles)
    # pprint(real)

tmpdata = pd.read_csv('../wiv_raw_data/C-S3-W130/110.dat',\
names = ['t', 'v', 'I', 'p', 'd','tmp'],\
skiprows = 1, sep='\t', header = None)
data = tmpdata.drop(['tmp'], axis=1) #delete tmp column.
print(tmpdata.v)

sum = 0
for i in data.v:
    sum = sum + i**2
# a = data.v**2
# b = a.sum()
# print((data.v**2).sum())
ohm = 10000
length = len(data.v)
Vrms = math.sqrt(sum)/length
power = Vrms**2 / ohm * 10**3
# print(power) # mW3


# for index,i in enumerate(data.v):
#     if abs(i)>1:
#         data.v[index]=100


#plt.plot(data.t,data.v)
#plt.show()
#data.plot(x=0,subplots=True,layout=(2,2))
#plt.plot(data.p,data.I,'ro')
#plt.show()

# r = data.corr('pearson')
# print(r)
#
#
#
#

# tmp = folderList + '/*.dat'
# fileList = glob.glob(tmp)
# print(fileList)



# for test in folderList:
#     splited = test.split('\\')[-1]
#     #print(splited)
#     tmp = test + '/*.dat'
#     pprint.pprint(tmp)
