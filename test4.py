import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
from scipy.fftpack import fft,fftfreq,ifft
from math import *
from pprint import pprint

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

vv=[[1,2],[4,5]]
vv = np.array(vv)
print(vv)

t = np.array(vv[:,0])
y = np.array(vv[:,1])

zero = len(t)*20
print(zero)
vv=np.pad(vv, ((zero,zero),(0,0)), 'constant', constant_values=0)
print(vv)
