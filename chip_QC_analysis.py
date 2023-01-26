import time
import sys
import csv
import os.path
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import statistics
import math
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
            y_count +=1

def read_num_col(file_csv):
    with open(file_csv, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for n in reader:
            return len(n)-2


#root_path_plot="/mnt/c/Users/antal/Documents/homework/QC_analysis_antalia/batch_001/RT/"
#root_path_plot="/mnt/c/Users/antal/Documents/homework/QC_analysis_antalia/batch_001/LN/"
root_path_plot="/mnt/c/Users/antal/Documents/homework/QC_analysis_antalia/"

file_table_power = root_path_plot + "Test_Summary_all_chip_power.csv"
file_table_bl = root_path_plot + "Test_Summary_all_chip_bl.csv"
file_table_inl = root_path_plot + "Test_Summary_all_chip_inl.csv"
file_table_noise = root_path_plot + "Test_Summary_all_chip_noise.csv"
file_table_noise_all_channel = root_path_plot + "Test_Summary_all_chip_noise_enc.csv"
file_table_vbgr = root_path_plot + "Test_Summary_all_chip_vbgr.csv"

col = read_num_col(file_table_power)

FE_bl_200=[]
for i in range(15):
    for j in range(col):
        FE_bl_200.append(read_cell(j+1,i+2,file_table_bl))

FE_bl_900=[]
for i in range(15):
    for j in range(col):
        FE_bl_900.append(read_cell(j+1,i+23,file_table_bl))

power_200mv=[]
for j in range(col):
    power_200mv.append(read_cell(j+1,2,file_table_power))

power_900mv=[]
for j in range(col):
    power_900mv.append(read_cell(j+1,8,file_table_power))

inl_200mv=[]
for i in range(15):
    for j in range(col):
        inl_200mv.append(read_cell(j+1,i+2,file_table_inl))

inl_900mv=[]
for i in range(15):
    for j in range(col):
        inl_900mv.append(read_cell(j+1,i+107,file_table_inl))

noise=[]
for i in range(15):
    for j in range(col):
        noise.append(read_cell(j+1,i+2,file_table_noise_all_channel))

vbgr=[]
for j in range(col):
    vbgr.append(read_cell(j+1,2,file_table_vbgr))

#mean
FE_bl_200mv_mean=statistics.mean(FE_bl_200)
FE_bl_900mv_mean=statistics.mean(FE_bl_900)
inl_200mv_mean=statistics.mean(inl_200mv)
inl_900mv_mean=statistics.mean(inl_900mv)
power_200mv_mean=statistics.mean(power_200mv)
power_900mv_mean=statistics.mean(power_900mv)
vbgr_mean=statistics.mean(vbgr)
noise_mean = statistics.mean(noise)

#sd
FE_bl_200mv_sd=statistics.stdev(FE_bl_200)
FE_bl_900mv_sd=statistics.stdev(FE_bl_900)
inl_200mv_sd=statistics.stdev(inl_200mv)
inl_900mv_sd=statistics.stdev(inl_900mv)
vbgr_sd=statistics.stdev(vbgr)
noise_sd = statistics.stdev(noise)
power_200mv_sd=statistics.stdev(power_200mv)
power_900mv_sd=statistics.stdev(power_900mv)

#3 sigma 200mv
FE_bl_sign_200 = FE_bl_200mv_mean - 3*FE_bl_200mv_sd
FE_bl_sigp_200 = FE_bl_200mv_mean + 3*FE_bl_200mv_sd

FE_bl_sign_900 = FE_bl_900mv_mean - 3*FE_bl_900mv_sd
FE_bl_sigp_900 = FE_bl_900mv_mean + 3*FE_bl_900mv_sd

inl_sign_200 = inl_200mv_mean - 3*inl_200mv_sd
inl_sigp_200 = inl_200mv_mean + 3*inl_200mv_sd

inl_sign_900 = inl_900mv_mean - 3*inl_900mv_sd
inl_sigp_900 = inl_900mv_mean + 3*inl_900mv_sd

power_sign_200 = power_200mv_mean - 3*power_200mv_sd
power_sigp_200 = power_200mv_mean + 3*power_200mv_sd

power_sign_900 = power_900mv_mean - 3*power_900mv_sd
power_sigp_900 = power_900mv_mean + 3*power_900mv_sd

vbgr_sign_200 = vbgr_mean - 3*vbgr_sd
vbgr_sigp_200 = vbgr_mean + 3*vbgr_sd

noise_sign_200 = noise_mean - 3*noise_sd
noise_sigp_200 = noise_mean + 3*noise_sd

#plotting
fig, ax = plt.subplots()

ax.set_ylabel('Normalized counts')

ax.set_xlabel('Baseline (mV)')

ax.set_title(f'Mean={power_200mv_mean:.2f},-3$\sigma$={power_sign_200:.2f},3$\sigma$={power_sigp_200:.2f}')
#ax.set_title(f'Mean={FE_bl_200mv_mean:.2f},-3$\sigma$={FE_bl_sign_200:.2f},3$\sigma$={FE_bl_sigp_200:.2f}')
#ax.set_title(f'Mean={FE_bl_900mv_mean:.2f},-3$\sigma$={FE_bl_sign_900:.2f},3$\sigma$={FE_bl_sigp_900:.2f}')

_, bins, _= plt.hist(power_200mv,10,density=True,rwidth=0.9,stacked=True)

avg=np.mean(power_200mv)
var=np.var(power_200mv)
pdf_x = np.linspace(np.min(power_200mv),np.max(power_200mv),100)
pdf_y = 1.0/np.sqrt(2*np.pi*var)*np.exp(-0.5*(pdf_x-avg)**2/var)

plt.plot(pdf_x,pdf_y)

#plt.legend([f'RMS:{FE_bl_200mv_sd:.2f}'])
plt.legend([f'RMS:{power_200mv_sd:.2f}'])
plt.show()
