import time
import sys
import pickle
import csv
import os.path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import statistics
import scipy
from scipy.stats import norm
def read_cell(x, y, file_csv):
    with open(file_csv, 'r') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return float(cell)

            y_count += 1

root_path_plot= "/mnt/c/Users/antal/Documents/homework/QC_analysis_antalia/"

file_table_power = root_path_plot + "Test_Summary_all_chip_power.csv"
file_table_bl = root_path_plot + "Test_Summary_all_chip_bl.csv"
file_table_inl = root_path_plot + "Test_Summary_all_chip_inl.csv"
file_table_noise = root_path_plot + "Test_Summary_all_chip_noise.csv"
file_table_gain = root_path_plot + "Test_Summary_all_chip_gain.csv"

power_200mv=[]
#SE=OFF SEDC=OFF
for j in range(1):
    power_200mv.append(read_cell(j+1,2,file_table_power))
    power_200mv.append(read_cell(j+1,3,file_table_power))
    power_200mv.append(read_cell(j+1,4,file_table_power))

FE_bl_200=[]
for i in range(17):
    for j in range(1):
        FE_bl_200.append(read_cell(j+1,i+2,file_table_bl))

inl_200mv=[]

for i in range(15):
    for j in range(1):
        inl_200mv.append(read_cell(j+1,i+2,file_table_inl))

noise=[]
for i in range(3):
    for j in range(1):
        noise.append(read_cell(j+1,i+2,file_table_noise))

gain=[]
for i in range(15):
    for j in range(1):
        gain.append(read_cell(j+1,i+2,file_table_gain))
#plt.plot(power_200mv)
#plt.plot(FE_bl_200)
#plt.plot(inl_200mv)
#plt.plot(noise)
plt.plot(noise)

plt.grid()
plt.show()
