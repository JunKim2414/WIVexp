from glob import glob
import math
import os
import pandas as pd
import matplotlib.pyplot as plt
import pprint
import numpy as np

class Project():
    def __init__(self, dir):
        self.project_directory = dir
        self.folderlist = {}
        self.Folder_reading()
        self.clustering()
        self.average()
        self.plotting_powering()

    def Folder_reading(self):
        folder_list = glob(self.project_directory)
        for folderdirectory in folder_list:
            Fd = Folder(folderdirectory)
            self.folderlist[Fd.casename] = Fd
            # Fd.plotting_powering()

    def clustering(self): # {C-S3-W130 : (C-S3-W130, C-S3-W130 (2))...}
        self.clustering = {}
        first_exp =[]
        re_exp=[]

        for key in self.folderlist:
            if '(' in key:
                re_exp.append(key)
            else:
                first_exp.append(key)

        for fst_exp_key in first_exp:
            self.clustering[fst_exp_key] = [self.folderlist[fst_exp_key]]
            for re_exp_key in re_exp:
                if fst_exp_key in re_exp_key:
                    self.clustering[fst_exp_key].append(self.folderlist[re_exp_key])
                    break

    def average(self):
        for test_name in self.clustering:
            power_list = []
            fst = self.clustering[test_name][0]
            scd = self.clustering[test_name][1]
            key = ['010','020','030','040','050','060','065','070','075','080','085','090','095','100','105','110']
            for i in key:
                try:
                    fst_file = fst.filelist[i]
                    scd_file = scd.filelist[i]
                    # print(fst_file.power,'&&', scd_file.power)
                    power_avg = (fst_file.power + scd_file.power)/2
                    # print(power_avg)
                    power_list.append(power_avg)
                except:
                    print(f'*** no key {i} ***')
            self.clustering[test_name].append(power_list)
        # pprint.pprint(self.clustering)

    def plotting_powering(self):
        for case in self.clustering:
            key = ['010','020','030','040','050','060','065','070','075','080','085','090','095','100','105','110']
            key_except = ['010','020','030','040','050','060','065','070','075','080','085','090','095','100','110']
            vel = [float(i)/100 for i in key]
            vel_except = [float(i)/100 for i in key_except]
            try:
                plt.plot(vel, self.clustering[case][2],lw=1,marker='*',markersize=5.0)


            except:
                plt.plot(vel_except, self.clustering[case][2],lw=1,marker='*',markersize=5.0 )

                # print(f'error at {case}')
                # pass
        plt.xlabel('V[m/s]')
        plt.ylabel('P[mW]')
        plt.xticks(np.arange(0, 1.2, 0.1))
        plt.grid(linestyle='--')
        plt.legend(self.clustering.keys())
        # plt.grid(True)
        plt.show()

class Folder():
    def __init__(self, dir):
        self.folder_directory = dir
        self.filelist = {}
        self.File_reading()
        self.parsing()

    def File_reading(self):
        filelist = glob(self.folder_directory+'/*.dat')
        for filedirectory in filelist:
            F = File(filedirectory)
            if F.velocity == 'initial':
                self.initial = F
            else:
                self.filelist[F.velocity] = F

    def parsing(self):
        foldername = os.path.basename(self.folder_directory).split('/')
        self.casename = foldername[-1]
        # print(foldername)

    # def plotting_powering(self):
    #     for i in self.filelist:
    #         file = self.filelist[i]
    #         plt.plot(float(i)/100, file.power, 'ro')
    #     plt.show()


class File():
    def __init__(self, dir):
        self.directory = dir
        self.parsing()
        self.analysis()
    def parsing(self):
        result = pd.read_csv(self.directory, sep='\t',\
        skiprows=1, names=['t','V','I','deg','torque','tmp'])
        result = result.drop(columns=['tmp'])
        result = result.apply(FileHandling_tool.Outlier_filter)
        self.data = result.apply(FileHandling_tool.Moving_averaging,window=10)
        filename = os.path.basename(self.directory).split('.')
        self.velocity = filename[0]

    def analysis(self):
        self.ohm = 10000
        self.Vrms = math.sqrt(sum([i**2 for i in self.data.V])/len(self.data.V))
        self.power = self.Vrms**2/self.ohm
        self.power = self.power * 1000

class FileHandling_tool():
    def Outlier_filter(series):
        mean = series.mean()
        std = series.std()
        tmp =[]
        for i in series:
            if i>mean-3*std and i<mean+3*std:
                tmp.append(i)
            else:
                tmp.append(0)
        tmp_series = pd.Series(tmp)
        return tmp_series
    def Moving_averaging(series,window):
        tmp = []
        window_value_list= []
        if series.name=='t':
            return series
        else:
            for i in series:
                window_value_list.append(i)
                if len(window_value_list)<window:
                    tmp.append(i)
                elif len(window_value_list)==window:
                    mean = sum(window_value_list)/len(window_value_list)
                    tmp.append(mean)
                else:
                    #longer than 'window'
                    window_value_list.pop(0) # eliminate first value in list
                    mean = sum(window_value_list)/len(window_value_list)
                    tmp.append(mean)
            return tmp

if __name__ == '__main__':
    project = Project('../wiv_raw_data/*')
    # Folder = Folder('../wiv_raw_data/C-S5-W047/*.dat')
    # Folder.plotting_powering()
