from matplotlib import pyplot as plt
import pandas as pd
import math

'''
x = range(-100, 101, 1)
y = []

for i in x:
    y_value = (i-30) * i * (i+70)
    y.append(y_value)

plt.plot(x, y, 'r-')
plt.show()
'''

'''
fileobj = open('./test.dat', 'w')
fileobj.write('is this real?\n')
fileobj.close()
'''

'''
t = 0
X = []
Y = []
T = []
n = range(1, 21, 2)
while t <= 4:
    x = 0
    y = 0
    for N in [math.pi * i for i in n]:
        x += 4/N*math.cos(N*t)
        y += 4/N*math.sin(N*t)
    X.append(x)
    Y.append(y)
    T.append(t)
    t += 0.005

fileobj = open('./write_array.dat', 'w')
for t,x,y in zip(T,X,Y):
    fileobj.write(f'{t:.4f} {x:.5f} {y:.5f}\n')
'''

'''
fig, axs = plt.subplots(1, 2)
axs[0].plot(X,Y,'r-')
axs[1].plot(T,Y,'b-')
plt.show()
'''

A = [{'x':0, 'y':1}, {'x':1, 'y':6}, {'x':6, 'y':3}]
dataframe = pd.DataFrame(A)
print(dataframe)
