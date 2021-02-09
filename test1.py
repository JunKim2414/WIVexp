import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
from scipy.fftpack import fft,fftfreq,ifft
from scipy.integrate import quad
from math import *

from pprint import  pprint
from copy import deepcopy

class Data_Loader():
    def __init__(self,file_directory):
        self.file_directory = file_directory
        self.parsing()

    def parsing(self):
        data = pd.read_csv(self.file_directory, sep = "\t", encoding = "utf-8")
        data = data.to_numpy()

        self.t = np.array(data[:,0])
        self.FP = np.array(data[:,1])
        self.AP = np.array(data[:,2])
        self.Probe = np.array(data[:,3])
        self.Surge = np.array(data[:,4])
        self.Res_wave = np.array(data[:,5])
        print('T length : {}'.format(len(self.t)))
        print('Probe length : {}'.format(len(self.Probe)))

        self.preprocessing()
    def preprocessing(self):
        self.plotting()
    def plotting(self):

        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(611)

        self.ax.plot(self.t, self.Surge, '-')
        self.ax.set_ylim(self.Surge.min(), self.Surge.max())
        self.ax.set_title('Surge')

        ax1 = self.fig.add_subplot(613)
        ax1.plot(self.t, self.AP, '-')
        ax1.set_ylim(self.AP.min(), self.AP.max())
        ax1.set_title('AP')

        ax2 = self.fig.add_subplot(614)
        ax2.plot(self.t, self.Probe, '-')
        ax2.set_ylim(self.Probe.min(), self.Probe.max())
        ax2.set_title('Probe')

        ax3 = self.fig.add_subplot(612)
        ax3.plot(self.t, self.FP, '-')
        ax3.set_ylim(self.FP.min(), self.FP.max())
        ax3.set_title('FP')

        ax4 = self.fig.add_subplot(615)
        ax4.plot(self.t, self.Res_wave, '-')
        ax4.set_ylim(self.Res_wave.min(), self.Res_wave.max())
        ax4.set_title('Res_wave')

        self.ax5 = self.fig.add_subplot(616)
        self.line5, = self.ax5.plot(self.t, self.Surge, '-')
        self.span = SpanSelector(self.ax, self.onselect, 'horizontal', useblit=True,rectprops=dict(alpha=0.5, facecolor='red'))
        plt.show()

    def onselect(self,tmin,tmax):
       indmin, indmax = np.searchsorted(self.t, (tmin, tmax))
       indmax = min(len(self.t) - 1, indmax)

       thist = self.t[indmin:indmax]
       thisFP = self.FP[indmin:indmax]
       thisAP = self.AP[indmin:indmax]
       thisProbe = self.Probe[indmin:indmax]
       thisSurge = self.Surge[indmin:indmax]
       thisRes_wave = self.Res_wave[indmin:indmax]
       self.line5.set_data(thist, thisSurge)
       self.ax5.set_xlim(thist[0], thist[-1])
       self.ax5.set_ylim(thisSurge.min(), thisSurge.max())
       self.fig.canvas.draw_idle()

       self.t = thist
       self.FP = thisFP
       self.AP = thisAP
       self.Probe = thisProbe
       self.Surge = thisSurge
       self.Res_wave = thisRes_wave
       print('자르고')
       print('T length : {}'.format(len(self.t)))
       print('Probe length : {}'.format(len(self.Probe)))

    def MovingAVG(self):
        self.LPP_m = 102/20
        self.dFP = 1.13
        self.dAP = 0.06
        self.dAFP = self.LPP_m - self.dFP - self.dAP
        self.Calm_RTM = 36.124
        self.Rhom = 998.02
        self.kinVm = 9.864E-07
        self.Vm = 1.553
        self.Bm = 0.910

        self.Pitch = (self.FP - self.AP)
        self.Heave = (1-(self.LPP_m-2*self.dFP)/(2*self.dAFP))*self.FP+((self.LPP_m-2*self.dFP)/(2*self.dAFP))*self.AP

        Pitch1 = self.Pitch - self.Pitch.mean()
        Pitch2 = pd.Series(Pitch1).rolling(8).mean()
        Pitch2 = np.array(Pitch2)
        for i in range(7):
            Pitch2[i] = self.Pitch[0]
        Pitch3 = np.array(180/pi*np.arctan(Pitch2/self.dAFP))

        Heave1 = self.Heave - self.Heave.mean()
        Heave2 = pd.Series(Heave1).rolling(8).mean()
        Heave2 = np.array(Heave2)
        for i in range(7):
            Heave2[i] = self.Heave[0]

        probe1 = self.Probe - self.Probe.mean()
        probe2 = pd.Series(probe1).rolling(8).mean()
        probe2 = np.array(probe2)
        for i in range(7):
            probe2[i] = self.Probe[0]

        Surge1 = self.Surge - self.Surge.mean()
        Surge2 = pd.Series(Surge1).rolling(8).mean()
        Surge2 = np.array(Surge2)
        for i in range(7):
            Surge2[i] = self.Surge[0]

        Res_wave1 = self.Res_wave
        Res_wave2 = pd.Series(Res_wave1).rolling(8).mean()
        Res_wave2 = np.array(Res_wave2)
        for i in range(7):
            Res_wave2[i] = self.Res_wave[0]

        self.Pitch = Pitch3
        self.Heave = Heave2
        self.Probe = probe2
        self.tempProbe = deepcopy(probe2)
        #for i in self.tempProbe:
            #print(i)
        self.Surge = Surge2
        self.Res_wave = Res_wave2
        self.RTM_wave = self.Res_wave.mean()

        print('이동평균')
        print('T length : {}'.format(len(self.t)))
        print('Probe length : {}'.format(len(self.Probe)))
    def FFT(self):
        self.MovingAVG()

        self.zero = len(self.t)*20
        #t3 = np.pad(self.t, ((self.zero,self.zero)), 'constant', constant_values=0)
        Pitch3 = np.pad(self.Pitch, ((self.zero,self.zero)), 'constant', constant_values=0)
        Heave3 = np.pad(self.Heave, ((self.zero,self.zero)), 'constant', constant_values=0)
        Probe3 = np.pad(self.Probe, ((self.zero,self.zero)), 'constant', constant_values=0)
        Surge3 = np.pad(self.Surge, ((self.zero,self.zero)), 'constant', constant_values=0)
        #self.t = t3
        self.Pitch = Pitch3
        self.Heave = Heave3
        self.Probe = Probe3
        self.Surge = Surge3

#Pitch FFT
        self.strength_Pitch = fft(self.Pitch)
        self.strength_Pitch = abs(self.strength_Pitch)*2/len(self.t)
        self.frequency_Pitch = fftfreq(self.Pitch.size, 0.005)
        mask = self.frequency_Pitch>=0

        #plt.plot(self.frequency_Pitch[mask], self.strength_Pitch[mask])
        #plt.show()

        self.PitchFrequency = self.frequency_Pitch[self.strength_Pitch.argmax()]
        self.MainPitch = max(self.strength_Pitch[mask])
        print(self.PitchFrequency, self.MainPitch)
#Heave FFT
        self.strength_Heave = fft(self.Heave)
        self.strength_Heave = abs(self.strength_Heave)*2/len(self.t)
        self.frequency_Heave = fftfreq(self.Heave.size, 0.005)
        mask = self.frequency_Heave>=0

        #plt.plot(self.frequency_Heave[mask], self.strength_Heave[mask])
        #plt.show()

        self.HeaveFrequency = self.frequency_Heave[self.strength_Heave.argmax()]
        self.MainHeave = max(self.strength_Heave[mask])
        print(self.HeaveFrequency, self.MainHeave)
#Surge FFT
        self.strength_Surge = fft(self.Surge)
        self.strength_Surge = abs(self.strength_Surge)*2/len(self.t)
        self.frequency_Surge = fftfreq(self.Surge.size, 0.005)
        mask = self.frequency_Surge>=0

        #plt.plot(self.frequency_Surge[mask], self.strength_Surge[mask])
        #plt.show()

        self.SurgeFrequency = self.frequency_Surge[self.strength_Surge.argmax()]
        self.MainSurge = max(self.strength_Surge[mask])
        print(self.SurgeFrequency, self.MainSurge)
#Probe FFT
        self.strength_Probe = fft(self.Probe)
        self.strength_Probe = abs(self.strength_Probe)*2/len(self.t)
        self.frequency_Probe = fftfreq(self.Probe.size, 0.005)
        mask = self.frequency_Probe>=0

        #plt.plot(self.frequency_Probe[mask], self.strength_Probe[mask])
        #plt.show()

        self.ENFrequency = self.frequency_Probe[self.strength_Probe.argmax()]
        self.ENwave = max(self.strength_Probe[mask])
        print(self.ENFrequency, self.ENwave)

        #print(self.RTM_wave)
#Fourier analysis
        print('FFT 이후')
        print('T length : {}'.format(len(self.t)))
        print('Probe length : {}'.format(len(self.Probe)))
        print('tempProbe length : {}'.format(len(self.tempProbe)))

        self.Te = 1/self.ENFrequency
        self.ENFrequency = self.ENFrequency
        self.Amp = self.ENwave/100
        self.RTM_wave = self.RTM_wave
        self.MainPitch = self.MainPitch
        self.MainHeave = self.MainHeave
        self.MainSurge = self.MainSurge

        self.Ti = 1/((sqrt(1+4*(1/self.Te)*(2*pi*self.Vm/9.81))-1)/(2*(2*pi*self.Vm/9.81)))
        self.LdofLPP = 9.81*(self.Ti**2)/(2*pi)/self.LPP_m
        self.CAW = (self.RTM_wave-self.Calm_RTM)/(self.Rhom*9.81*self.Amp**2*self.Bm**2/self.LPP_m)
        self.RAO_Heave = self.MainHeave/self.Amp
        self.RAO_Pitch = (self.MainPitch*pi/180)/(self.Amp*(2*pi/(self.LdofLPP*self.LPP_m)))
        self.RAO_Surge = self.MainSurge/self.Amp

        print(self.Amp, self.Ti, self.LdofLPP, self.CAW, self.RAO_Heave, self.RAO_Pitch, self.RAO_Surge)

#    def FourierAnalysis(self):
        #for i, j in zip(self.t, self.tempProbe):

    #    F, err = quad(f, 0, len(self.t))

        #self.MovingAVG()
        #print(self.tempProbe)
        #self.Probe = self.Probe + self.Probe.mean()

        #for k in [1]:
        #    self.An = 0
        #    self.Bn = 0
#
#            for i, j in zip(self.t, self.tempProbe):
#                self.An = self.An + (2/len(self.tempProbe))*(j*cos(2*np.pi*i*k*self.ENFrequency))
#                self.Bn = self.Bn + (2/len(self.tempProbe))*(j*sin(2*np.pi*i*k*self.ENFrequency))
#            self.Dn = sqrt(self.An**2+self.Bn**2)
#        print(self.Dn)

        #for k in self.tempProbe:
            #print(k)
            #if k==temp:
            #    pass
        #    else:
            #    print(k)
                #temp = k

#        plt.plot(self.t,self.tempProbe)
#        plt.show()
#        print(self.t, self.tempProbe)
#        print(self.An)
#        print(self.Bn)
#        print(self.Dn)
       #np.savetxt("D201028WL11N01(range).dat", np.c_[thist, thisFP, thisAP, thisProbe, thisSurge, thisRes_wave], delimiter = '\t',  fmt='%.3f')
data_loader = Data_Loader('./D200903WL09N02.dat')
#data_loader.MovingAVG()
data_loader.FFT()
#data_loader.FourierAnalysis()
