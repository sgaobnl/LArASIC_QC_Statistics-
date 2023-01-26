 # -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 15:46:33 2021

@author: Eaglekumar
"""

#import dual_dut_preset as preset
import time
import sys
import pickle
import csv
import os.path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
def read_cell(x, y, file_csv):
    with open(file_csv, 'r') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1
            

start_time = time.time()
import datetime
from datetime import datetime, date

Date_today = datetime.now().strftime('%m-%d-%Y')# %H:%M:%S
print(Date_today)
#socket_no = int(sys.argv[1])  # socket number
socket_no=0
board_ID = "DUAL_DUT"

Cd="0pF"#"0pF"
fontsize_no=8
temperature = "RT" #LN  #RT
#root_path= "F:/DUAL DUT/QC_Results_Dual_DUT_2/"
#root_path = "E:/LArASIC_P5_QC/Test_results/"
#root_path_plot=root_path+ "QC_LArASIC_results_combined_RT/"

#root_path="/mnt/c/Users/antal/Documents/homework/QC_analysis_antalia/LArASIC_P5B_Batch_001/RT/"
#root_path = "/mnt/c/Users/antal/Documents/homework/QC_analysis_antalia/LArASIC_P5B_QC_new_Batch_2022/LN/"
#root_path_plot = "/mnt/c/Users/antal/Documents/homework/QC_analysis_antalia/LArASIC_P5B_QC_new_Batch_2022/"

root_path = "/mnt/c/Users/antal/Documents/homework/QC_analysis_antalia/QC_analysis/"
root_path_plot="/mnt/c/Users/antal/Documents/homework/QC_analysis_antalia/"

Chip_name='P5B'

FE_chip_dis="FEChip_"+ Chip_name + "_"
x_label_dis=Chip_name + ' LArASIC Chip#'

if os.path.exists(root_path_plot):
    pass
else:
    try:
        os.makedirs(root_path_plot)
    except OSError:
        print ("Error to create folder ")
        sys.exit()
        
        
ColdADC_chip_id = "ColdADC_P2_60"

file_table_power = root_path_plot + "Test_Summary_all_chip_power.csv"
file_table_bl = root_path_plot + "Test_Summary_all_chip_bl.csv"
file_table_vbgr = root_path_plot + "Test_Summary_all_chip_vbgr.csv"
file_table_temp = root_path_plot + "Test_Summary_all_chip_temp.csv"

file_table_chresp = root_path_plot + "Test_Summary_all_chip_response.csv"
file_table_chresp_ext = root_path_plot + "Test_Summary_all_chip_response_ext.csv"

file_table_noise = root_path_plot + "Test_Summary_all_chip_noise.csv"
file_table_noise_enc= root_path_plot + "Test_Summary_all_chip_noise_enc.csv"
file_table_gain = root_path_plot + "Test_Summary_all_chip_gain.csv"
file_table_inl = root_path_plot + "Test_Summary_all_chip_inl.csv"

file_table_failed_chip = root_path_plot + "Test_Summary_Failed_chip.csv"
file_table_failed_chip_detail = root_path_plot + "Test_Summary_Failed_chip_detail.csv"

# Power table initialization
power_col_900=[]         
buf_state=["Chip#", "SE=OFF SEDC=OFF", "SE=ON SEDC=OFF", "SE=OFF SEDC=ON"]
power_col_900.append(buf_state)
power_900mv_1=[]
power_900mv_2=[]
power_900mv_3=[]
chip_id=[]

#
#chip_list=[]
#chip_list=['05', '06']
chip_list=['416', '420','421','425','448','452','453','457','485','489']
chip_list_l0=[]
remove_chip_list=[]
remove_chip_list=[]#['01', '39', '44', '41']#['216', '268', '272']
#for chip_no in range(0, 536, 1):
for chip_no in range(0, 900, 1):
#for chip_no in chip_list:
    FE_chip_no=str(chip_no)
    FE_chip_no.zfill(2)
    #if (chip_no<10):
        #FE_chip_no= "{:0>2}".format(FE_chip_no)
    FE_chip_no="00100"+"{:0>3}".format(FE_chip_no)
    FE_chip_id=FE_chip_dis + FE_chip_no
    chip_rawdir = root_path + "Board_" + board_ID + "_"  + FE_chip_id  + "_" +  temperature + "/"
    if os.path.exists(chip_rawdir):
        pass
        chip_list_l0.append(FE_chip_no)

#print(chip_list_l0)
#for the 4 zeroes
for chip_no in range(0, 931, 1):
#for chip_no in chip_list:
    FE_chip_no=str(chip_no)
    FE_chip_no.zfill(4)
    #if (chip_no<10):
        #FE_chip_no= "{:0>2}".format(FE_chip_no)
    FE_chip_no="00100"+"{:0>4}".format(FE_chip_no)
    FE_chip_id=FE_chip_dis + FE_chip_no
    chip_rawdir = root_path + "Board_" + board_ID + "_"  + FE_chip_id  + "_" +  temperature + "/"
    if os.path.exists(chip_rawdir):
        pass
        chip_list_l0.append(FE_chip_no)
    #print(FE_chip_no)

chip_list = [ele for ele in chip_list if ele not in remove_chip_list]
#print(len(chip_list), chip_list)        
#chip_list=['05', '06']

for chip_no in chip_list_l0:
    #print(chip_no)
    chip_id.append(chip_no)
    FE_chip_no=str(chip_no)

    FE_chip_id = FE_chip_dis + FE_chip_no
    
    chip_rawdir = root_path + "Board_" + board_ID + "_"  + FE_chip_id  + "_" +  temperature + "/"
    #print(chip_rawdir)
    if os.path.exists(chip_rawdir):
        pass
    else:
        try:
            os.makedirs(chip_rawdir)
        except OSError:
            print ("Error to create folder ")
            sys.exit()
    para_rawdir = chip_rawdir + "Power_measurement/" 
    #print(para_rawdir)
    if os.path.exists(para_rawdir):
        pass
        file_csv=para_rawdir  + "Power_" +  FE_chip_id + ".csv"
        power_900mv_1.append(read_cell(1, 5, file_csv))
        power_900mv_2.append(read_cell(1, 7*1+5, file_csv))
        power_900mv_3.append(read_cell(1, 7*2+5, file_csv))
       
        #print(power_900mv_1)
        power_val=[FE_chip_no, read_cell(1, 5, file_csv), read_cell(1, 7*1+5, file_csv), read_cell(1, 7*2+5, file_csv)]
        power_col_900.append(power_val)
        #print(power_val)
    else:
        print ("Measuremnets data related to power is not available ")

# Power table initialization
power_col_200=[]
power_200mv_1=[]
power_200mv_2=[]
power_200mv_3=[]
chip_id=[]         
buf_state=["Chip#", "SE=OFF SEDC=OFF", "SE=ON SEDC=OFF", "SE=OFF SEDC=ON"]
power_col_200.append(buf_state)
    
for chip_no in chip_list_l0:
    FE_chip_no=str(chip_no)
    chip_id.append(chip_no)
    FE_chip_id=FE_chip_dis + FE_chip_no
    
    chip_rawdir = root_path + "Board_" + board_ID + "_"  + FE_chip_id  + "_" +  temperature + "/"
    if os.path.exists(chip_rawdir):
        pass
    else:
        try:
            os.makedirs(chip_rawdir)
        except OSError:
            print ("Error to create folder ")
            sys.exit()
    
    para_rawdir = chip_rawdir + "Power_measurement/" 
    #print(para_rawdir)
    if os.path.exists(para_rawdir):
        pass
        file_csv=para_rawdir  + "Power_" +  FE_chip_id + ".csv"
        power_200mv_1.append(read_cell(1, 7*3+5, file_csv))
        power_200mv_2.append(read_cell(1, 7*4+5, file_csv))
        power_200mv_3.append(read_cell(1, 7*5+5, file_csv))

        power_val=[FE_chip_no, read_cell(1, 7*3+5, file_csv), read_cell(1, 7*4+5, file_csv), read_cell(1, 7*5+5, file_csv)]
        power_col_200.append(power_val) 
    else:
        print ("Measuremnets data related to power is not available ")

heading=["Power Measurements", "200mV BL"]   
rows=zip(*power_col_200) 
with open(file_table_power, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()
    
heading=["Power Measurements", "900mV BL"]   
rows=zip(*power_col_900) 
with open(file_table_power, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()

power_list=[]
#print(power_200mv_1)
for bl in ['200mV', '900mV']:
    for buf in ['SE_OFF_SEDC_OFF', 'SE_ON_SEDC_OFF', 'SE_OFF_SEDC_ON']:
        if bl=='200mV':
            if buf=='SE_OFF_SEDC_OFF':    
                power_list=power_200mv_1
                title_lab='SE=OFF, SEDC=OFF'
            elif  buf=='SE_ON_SEDC_OFF':
                power_list=power_200mv_2
                title_lab='SE=ON, SEDC=OFF'
            elif  buf=='SE_OFF_SEDC_ON':
                power_list=power_200mv_3
                title_lab='SE=OFF, SEDC=ON'
        else:
            if buf=='SE_OFF_SEDC_OFF':    
                power_list=power_900mv_1
                title_lab='SE=OFF, SEDC=OFF'
            elif  buf=='SE_ON_SEDC_OFF':
                power_list=power_900mv_2
                title_lab='SE=ON, SEDC=OFF'
            elif  buf=='SE_OFF_SEDC_ON':
                power_list=power_900mv_3
                title_lab='SE=OFF, SEDC=ON'
        labels = chip_list
        x_pos = np.arange(len(labels))
        #mean_y  = [(float(i)) for i in power_list]
        #print(x_pos, (labels), (mean_y))
        fig, ax = plt.subplots()
        #ax.bar(x_pos, mean_y,
               #yerr=0,
               #align='center',
               #alpha=0.5,
               #ecolor='black',
               #capsize=2)
        ax.set_ylabel('Power (mW/Ch)')
        ax.set_xlabel(x_label_dis)
        ax.set_ylim(0, 15)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
        ax.set_title('Dt:' + Date_today + '\n LArASIC Power, ' + bl + ', ' + title_lab)
        ax.yaxis.grid(True)
        plt.tight_layout()
        #plt.savefig(root_path_plot + "Power_"+ bl + "_" + buf + ".png")
        plt.close()

labels = chip_list
x_pos = np.arange(len(labels))
#mean_y  = [(float(i)) for i in power_200mv_1]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=0,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('Power (mW/Ch)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(0, 15)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n LArASIC Power, 200mV BL, SE=OFF, SEDC=OFF')
ax.yaxis.grid(True)
plt.tight_layout()
#plt.savefig(root_path_plot + 'Power_200mV.png')
plt.close()

# FE parmeter table initialization
FE_bl_200=[]
FE_bl_col0=[]         
FE_bl_col0.append("Ch#/Chip#")
for i in range (16):
    FE_bl_col0.append(str(i))
FE_bl_col0.append("Mean")
FE_bl_col0.append("SD")
#print(FE_bl_col0)
FE_bl_200.append(FE_bl_col0)

FE_bl_900=[]
FE_bl_col0=[]         
FE_bl_col0.append("Ch#/CHip#")
for i in range (16):
    FE_bl_col0.append(str(i))
FE_bl_col0.append("Mean")
FE_bl_col0.append("SD")
#print(FE_bl_col0)
FE_bl_900.append(FE_bl_col0)

FE_bl_vbgr1=[]
FE_bl_temp1=[]

chip_id=[]         
FE_bl_200mv_mean=[]
FE_bl_200mv_sd=[]
FE_bl_900mv_mean=[]
FE_bl_900mv_sd=[]
FE_bl_vbgr2=[]
                   
for chip_no in chip_list_l0:
    chip_id.append(chip_no)
    FE_chip_no=str(chip_no)
    
    FE_chip_id=FE_chip_dis + FE_chip_no
    
    chip_rawdir = root_path + "Board_" + board_ID + "_"  + FE_chip_id  + "_" +  temperature + "/"
    if os.path.exists(chip_rawdir):
        pass
    else:
        try:
            os.makedirs(chip_rawdir)
        except OSError:
            print ("Error to create folder ")
            sys.exit()
    
    para_rawdir = chip_rawdir + "FE_Parameter_test/" 
    if os.path.exists(para_rawdir):
        pass
        file_csv=para_rawdir  + "Baseline_VBGR_Temp_" +  FE_chip_id + ".csv"


        FE_bl_vbgr=[]
        FE_bl_temp=[]
        FE_bl_vbgr.append(FE_chip_no)
        FE_bl_temp.append(FE_chip_no)
        
        FE_bl_200mv_mean.append(read_cell(1, 17, file_csv))
        FE_bl_200mv_sd.append(read_cell(1, 18, file_csv))
        FE_bl_900mv_mean.append(read_cell(2, 17, file_csv))
        FE_bl_900mv_sd.append(read_cell(2, 18, file_csv))
        FE_bl_vbgr.append(read_cell(1, 20, file_csv))
        FE_bl_vbgr2.append(read_cell(1, 20, file_csv))
        FE_bl_temp.append(read_cell(1, 21, file_csv))
        temp=[]
        temp1=[]
        temp.append(FE_chip_no)
        temp1.append(FE_chip_no)
        for i in range(18):
            temp.append(read_cell(1, i+1, file_csv))
            temp1.append(read_cell(2, i+1, file_csv))
            
        FE_bl_200.append(temp)
        FE_bl_900.append(temp1)
        FE_bl_vbgr1.append(FE_bl_vbgr)
        FE_bl_temp1.append(FE_bl_temp)

        
    else:
        print ("Measuremnets data related to power is not available ")

heading=["Basline Measurements", "200mV BL"]   
rows=zip(*FE_bl_200) 
with open(file_table_bl, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()

heading=["Basline Measurements", "900mV BL"]   
rows=zip(*FE_bl_900) 
with open(file_table_bl, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()

heading=["VBGR"]   
rows=zip(*FE_bl_vbgr1) 
with open(file_table_vbgr, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()

heading=["Temp"]   
rows=zip(*FE_bl_temp1) 
with open(file_table_temp, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()

labels = chip_list
x_pos = np.arange(len(labels))
mean_y  = [(float(i)) for i in FE_bl_200mv_mean]
error_y = [(float(i)) for i in FE_bl_200mv_sd]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=error_y,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('Baseline (mV)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(0, 350)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n 200mV Baseline')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
#plt.savefig(root_path_plot + 'Baseline_200mV.png')
plt.close()

labels = chip_list
x_pos = np.arange(len(labels))
mean_y  = [(float(i)) for i in FE_bl_900mv_mean]
error_y = [(float(i)) for i in FE_bl_900mv_sd]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=error_y,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('Baseline (mV)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(700, 1050)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n 900mV Baseline')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
#plt.savefig(root_path_plot + 'Baseline_900mV.png')
plt.close()

labels = chip_list
x_pos = np.arange(len(labels))
mean_y  = [(float(i)) for i in FE_bl_vbgr2]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=0,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('VBGR (V)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(0, 1.5)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n VBGR')
ax.yaxis.grid(True)

# Save the figue and show
plt.tight_layout()
#plt.savefig(root_path_plot + 'VBGR.png')
plt.close()


# noise table initialization
FE_noise=[]
FE_n_col0=[]         
FE_n_col0=["Tp/Chip#", "0.5us", "1us", "2us", "3us"]
FE_noise.append(FE_n_col0)
#print(FE_bl_col0)

chip_id=[]         
FE_noise1=[[],[],[],[]]
FE_noisesd1=[[],[],[],[]]

FE_noise0=[[],[],[],[]]
FE_noisesd0=[[],[],[],[]]
                   
for chip_no in chip_list_l0:
    chip_id.append(chip_no)
    FE_chip_no=str(chip_no)
    
    FE_chip_id=FE_chip_dis + FE_chip_no
    
    chip_rawdir = root_path + "Board_" + board_ID + "_"  + FE_chip_id  + "_" +  temperature + "/"
    if os.path.exists(chip_rawdir):
        pass
    else:
        try:
            os.makedirs(chip_rawdir)
        except OSError:
            print ("Error to create folder ")
            sys.exit()
    
    noise_rawdir = chip_rawdir + "Noise_measurement/" + FE_chip_id + "_" + Cd + "/result/"
    if os.path.exists(noise_rawdir):
        pass
        file_csv=noise_rawdir  + "Noise_ENC_raw.csv"
        temp=[]
        temp1=[]
        temp.append(FE_chip_no)
        for i in range(4):
            for j in range(15):
                temp.append(read_cell(1+i, j+1, file_csv))
                FE_noise1[i].append(read_cell(1+i, 17, file_csv))
                FE_noisesd1[i].append(read_cell(1+i, 18, file_csv))
        FE_noise.append(temp)
    else:
        print ("Measuremnets data related to power is not available ")

heading=["Noise Measurements", Cd]   
rows=zip(*FE_noise) 
with open(file_table_noise, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()

#labels = chip_list
#width = 0.10
#x_pos = np.arange(len(labels))
#mean_y  = [int(float(i)) for i in FE_noise1[0]]
#error_y = [int(float(i)) for i in FE_noisesd1[0]]
#fig, ax = plt.subplots()
#ax.bar(x_pos-2*width/4, mean_y,
#       yerr=error_y,
#       #align='center',
#       #alpha=0.5,
#       width=width/4,
#       label='0.5us',
#       ecolor='black',
#       capsize=5
#       )
#
#mean_y  = [int(float(i)) for i in FE_noise1[1]]
#error_y = [int(float(i)) for i in FE_noisesd1[1]]
#ax.bar(x_pos-1*width/4, mean_y,
#       yerr=error_y,
#       #align='center',
#       #alpha=0.5,
#       width=width/4,
#       label='1us',
#       ecolor='black',
#       capsize=5
#       )
#
#mean_y  = [int(float(i)) for i in FE_noise1[2]]
#error_y = [int(float(i)) for i in FE_noisesd1[2]]
#ax.bar(x_pos+0*width/4, mean_y,
#       yerr=error_y,
#       #align='center',
#       #alpha=0.5,
#       width=width/4,
#       label='2us',
#       ecolor='black',
#       capsize=5
#       )
#
#mean_y  = [int(float(i)) for i in FE_noise1[3]]
#error_y = [int(float(i)) for i in FE_noisesd1[3]]
#ax.bar(x_pos+1*width/4, mean_y,
#       yerr=error_y,
#       #align='center',
#       #alpha=0.5,
#       width=width/4,
#       label='3us',
#       ecolor='black',
#       capsize=5
#       )
#
#
#ax.set_ylabel('Noise (e-)')
#ax.set_xlabel('P5 LArASIC Chip#')
##ax.set_ylim(0, 200)
#ax.set_xticks(x_pos)
#ax.set_xticklabels(labels)
#ax.set_title('Noise (ENC)')
#ax.yaxis.grid(True)
#
## Save the figure and show
##plt.xticks(x_pos + width/2, labels)
#
#plt.tight_layout()
#plt.savefig(root_path_plot + 'Noise_ENC.png')

labels = chip_list
x_pos = np.arange(len(labels))
mean_y  = [int(float(i)) for i in FE_noise1[0]]
error_y = [int(float(i)) for i in FE_noisesd1[0]]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=error_y,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('Noise (e-)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(0, 1500)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n Noise (ENC) @ Tp=0.5us')
ax.yaxis.grid(True)
plt.tight_layout()
#plt.savefig(root_path_plot + 'Noise_ENC_05us.png')
plt.close()

labels = chip_list
x_pos = np.arange(len(labels))
mean_y  = [int(float(i)) for i in FE_noise1[1]]
error_y = [int(float(i)) for i in FE_noisesd1[1]]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=error_y,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('Noise (e-)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(0, 1500)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n Noise (ENC) @ Tp=1us')
ax.yaxis.grid(True)
plt.tight_layout()
#plt.savefig(root_path_plot + 'Noise_ENC_10us.png')
plt.close()

labels = chip_list
x_pos = np.arange(len(labels))
mean_y  = [int(float(i)) for i in FE_noise1[2]]
error_y = [int(float(i)) for i in FE_noisesd1[2]]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=error_y,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('Noise (e-)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(0, 1500)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n Noise (ENC) @ Tp=2us')
ax.yaxis.grid(True)
plt.tight_layout()
#plt.savefig(root_path_plot + 'Noise_ENC_20us.png')
plt.close()

labels = chip_list
x_pos = np.arange(len(labels))
mean_y  = [int(float(i)) for i in FE_noise1[3]]
error_y = [int(float(i)) for i in FE_noisesd1[3]]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=error_y,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('Noise (e-)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(0, 1500)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n Noise (ENC) @ Tp=3us')
ax.yaxis.grid(True)
plt.tight_layout()
#plt.savefig(root_path_plot + 'Noise_ENC_30us.png')
plt.close()

#noise enc 1us
FE_noise_enc=[]
FE_noise_enc1=[]
FE_noise_enc2=[]
FE_noise_enc3=[]
for chip_no in chip_list_l0:
    chip_id.append(chip_no)
    FE_chip_no=str(chip_no)

    FE_chip_id=FE_chip_dis + FE_chip_no

    chip_rawdir = root_path + "Board_" + board_ID + "_"  + FE_chip_id  + "_" +  temperature + "/"
    if os.path.exists(chip_rawdir):
        pass
    else:
        try:
            os.makedirs(chip_rawdir)
        except OSError:
            print ("Error to create folder ")
            sys.exit()

    noise_rawdir = chip_rawdir + "Noise_measurement/" + FE_chip_id + "_" + Cd + "/result/"
    if os.path.exists(noise_rawdir):
        pass
        file_csv=noise_rawdir  + "Noise_ENC_raw.csv"
        temp=[]
        temp1=[]
        temp2=[]
        temp3=[]
        temp.append(FE_chip_no)
        temp1.append(FE_chip_no)
        temp2.append(FE_chip_no)
        temp3.append(FE_chip_no)
        #for i in range(4):
        for j in range(15):
            temp.append(read_cell(1, j+1, file_csv)) #3,2,1
            FE_noise1[i].append(read_cell(4, 17, file_csv)) #3,2,1
            FE_noisesd1[i].append(read_cell(4, 18, file_csv)) #3,2,1

            temp1.append(read_cell(2, j+1, file_csv))
            temp2.append(read_cell(3, j+1, file_csv))
            temp3.append(read_cell(4, j+1, file_csv))

        FE_noise_enc.append(temp)
        FE_noise_enc1.append(temp1)
        FE_noise_enc2.append(temp2)
        FE_noise_enc3.append(temp3)
        #temp.clear()
    else:
        print ("Measuremnets data related to power is not available ")

heading=["Noise Measurements", Cd, "0.5us"]
rows=zip(*FE_noise_enc)
with open(file_table_noise_enc, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

#added
heading=["Noise Measurements", Cd, "1us"]
rows=zip(*FE_noise_enc1)
with open(file_table_noise_enc, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

heading=["Noise Measurements", Cd, "2us"]
rows=zip(*FE_noise_enc2)
with open(file_table_noise_enc, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

heading=["Noise Measurements", Cd, "3us"]
rows=zip(*FE_noise_enc3)
with open(file_table_noise_enc, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

# FE Channel response table
FE_res_200mv=[]
FE_res_900mv=[]
FE_res_200mv_sdd=[]
 
FE_res_200=[]
FE_res_col0=[]         
FE_res_col0.append("Ch#/Chip#")
for i in range (16):
    FE_res_col0.append(str(i))
#print(FE_res_col0)
FE_res_200mv.append(FE_res_col0)
FE_res_200mv_sdd.append(FE_res_col0)

FE_res_900=[]
FE_res_col0=[]         
FE_res_col0.append("Ch#/Chip#")
for i in range (16):
    FE_res_col0.append(str(i))
#print(FE_res_col0)
FE_res_900mv.append(FE_res_col0)




chip_id=[]         
Ch_res_200=[]
Ch_res_200_str=[]
Ch_res_900=[]
Ch_res_900_str=[]
Ch_res_200_on=[]
Ch_res_200_on_str=[]                 
Failed_chs_res_chip=[]
Failed_chs_res_chip_200=[]
Failed_chs_res_chip_900=[]
Failed_chs_res_chip_sddon=[]
Failed_chs_res_chip_ext=[]

Failed_chs_res_chip_200.append('200mV BL')
Failed_chs_res_chip_900.append('900mV BL')
Failed_chs_res_chip_sddon.append('SDD ON, Diff')
Failed_chs_res_chip_ext.append('Ext pulse')

for chip_no in chip_list_l0:
    chip_id.append(chip_no)
    FE_chip_no=str(chip_no)
    
    FE_chip_id=FE_chip_dis + FE_chip_no
    
    chip_rawdir = root_path + "Board_" + board_ID + "_"  + FE_chip_id  + "_" +  temperature + "/"
    if os.path.exists(chip_rawdir):
        pass
    else:
        try:
            os.makedirs(chip_rawdir)
        except OSError:
            print ("Error to create folder ")
            sys.exit()
    
    para_rawdir = chip_rawdir + "Channel_Response/" 
    if os.path.exists(para_rawdir):
        pass
        file_csv=para_rawdir  + "Channel_Response_result_DACpls_900mV_200mV_SEDC_OFF"  + ".csv"
        sts_200mV=[]
        sts_200=0
        sts_900=0
        sts_200_on=0
        sts_200mV.append(FE_chip_no)
        for i in range (16):
            for col in range(4):
                status=read_cell(col+1, 2+i, file_csv)
                if (status== "Failed"):
                  sts_200mV.append("Failed")
                  sts_200=1
                else:
                    if (col==3):
                        sts_200mV.append("Passed")    
        sts_900mV=[]
        sts_900mV.append(FE_chip_no)
        for i in range (16):
            for col in range(4):
                status=read_cell(col+1, 21+i, file_csv)
                if (status== "Failed"):
                  sts_900mV.append("Failed")
                  sts_900=1
                else:
                    if (col==3):
                        sts_900mV.append("Passed")    
        FE_res_200mv.append(sts_200mV)
        FE_res_900mv.append(sts_900mV)
        
        file_csv=para_rawdir  + "Channel_Response_result_DACpls_200mV_SEDC_ON"  + ".csv"
        sts_200mV=[]
        sts_200mV.append(FE_chip_no)
        for i in range (16):
            status=read_cell(1, 2+i, file_csv)
            if (status== "Failed"):
                sts_200mV.append("Failed")
                sts_200_on=1
            else:
                sts_200mV.append("Passed")
        FE_res_200mv_sdd.append(sts_200mV)
        
        if (sts_200==1):
            Ch_res_200.append("2")
            Ch_res_200_str.append("D")
        else:
            Ch_res_200.append("1")
            Ch_res_200_str.append("A")
        if (sts_900==1):
            Ch_res_900.append("2")
            Ch_res_900_str.append("D")
        else:
            Ch_res_900.append("1")
            Ch_res_900_str.append("A")
        if (sts_200_on==1):
            Ch_res_200_on.append("2")
            Ch_res_200_on_str.append("D")
        else:
            Ch_res_200_on.append("1")
            Ch_res_200_on_str.append("A")
            
        if (sts_200==1) or (sts_900==1) or (sts_200_on==1):
            Failed_chs_res_chip.append(FE_chip_no)
        if (sts_200==1):
           Failed_chs_res_chip_200.append(FE_chip_no)
        else:
           Failed_chs_res_chip_200.append('') 
        if (sts_900==1):
           Failed_chs_res_chip_900.append(FE_chip_no)
        else:
           Failed_chs_res_chip_900.append('')    
        if (sts_200_on==1):
           Failed_chs_res_chip_sddon.append(FE_chip_no) 
        else:
           Failed_chs_res_chip_sddon.append('')               
                         
    else:
        print ("Measuremnets data related to channel response is not available ")


    
heading=["200mV BL", "SEDC OFF"]   
rows=zip(*FE_res_200mv) 
with open(file_table_chresp, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()

heading=[ "900mV BL", "SEDC OFF"]     
rows=zip(*FE_res_900mv) 
with open(file_table_chresp, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()

heading=[ "200mV BL", "SEDC ON"]     
rows=zip(*FE_res_200mv_sdd) 
with open(file_table_chresp, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()

labels = chip_list
x_pos = np.arange(len(labels))
y_pos=["Alive", "Dead"]
mean_y  = [(float(i)) for i in Ch_res_200]
error_y = [(float(i)) for i in Ch_res_200]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=0,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('Channel Response (Alive/Dead)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(0, 3)
#ax.set_yticks(y_pos)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n Channel Response, 200mV BL, SEDC=OFF, A=Alive, D=Dead')
ax.yaxis.grid(True)
#for i in range(len(x_pos)):
    #plt.annotate(str(Ch_res_200_str[i]) , xy=(x_pos[i], mean_y[i]), ha='center', va='bottom')
#plt.tight_layout()
#plt.savefig(root_path_plot + 'Channel_Response_200mV.png')
plt.close()


labels = chip_list
x_pos = np.arange(len(labels))
y_pos=["Alive", "Dead"]
mean_y  = [(float(i)) for i in Ch_res_900]
error_y = [(float(i)) for i in Ch_res_900]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=0,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('Channel Response (Alive/Dead)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(0, 3)
#ax.set_yticks(y_pos)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n Channel Response, 900mV BL, SEDC=OFF, A=Alive, D=Dead')
ax.yaxis.grid(True)
#for i in range(len(x_pos)):
    #plt.annotate(str(Ch_res_900_str[i]) , xy=(x_pos[i], mean_y[i]), ha='center', va='bottom')
plt.tight_layout()
#plt.savefig(root_path_plot + 'Channel_Response_900mV.png')
plt.close()



labels = chip_list
x_pos = np.arange(len(labels))
y_pos=["Alive", "Dead"]
mean_y  = [(float(i)) for i in Ch_res_200_on]
error_y = [(float(i)) for i in Ch_res_200_on]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=0,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('Channel Response (Alive/Dead)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(0, 3)
#ax.set_yticks(y_pos)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n Channel Response, 200mV BL, SEDC=ON, A=Alive, D=Dead')
ax.yaxis.grid(True)
#for i in range(len(x_pos)):
    #plt.annotate(str(Ch_res_200_on_str[i]) , xy=(x_pos[i], mean_y[i]), ha='center', va='bottom')
#plt.tight_layout()
#plt.savefig(root_path_plot + 'Channel_Response_200mV_SDD_ON.png')
plt.close()


Ch_res_200=[]
Ch_res_200_str=[]

# FE Channel response Ext
FE_res_200mv=[]
 
FE_res_200=[]
FE_res_col0=[]         
FE_res_col0.append("Ch#/Chip#")
for i in range (16):
    FE_res_col0.append(str(i))
#print(FE_res_col0)
FE_res_200mv.append(FE_res_col0)

chip_id=[]         

                   
for chip_no in chip_list_l0:
    chip_id.append(chip_no)
    FE_chip_no=str(chip_no)
    
    FE_chip_id=FE_chip_dis + FE_chip_no
    
    chip_rawdir = root_path + "Board_" + board_ID + "_"  + FE_chip_id  + "_" +  temperature + "/"
    if os.path.exists(chip_rawdir):
        pass
    else:
        try:
            os.makedirs(chip_rawdir)
        except OSError:
            print ("Error to create folder ")
            sys.exit()
    
    para_rawdir = chip_rawdir + "Channel_Response_Ext_Pulse/" 
    if os.path.exists(para_rawdir):
        pass
        file_csv=para_rawdir  + "Channel_Response_result_Extpls_200mV_SEDC_OFF"  + ".csv"
        sts_200mV=[]
        sts_200=0
        sts_200mV.append(FE_chip_no)
        #for i in range (16):
            #status=read_cell(1, 1+i, file_csv)
            #if (status== "Failed"):
                #sts_200mV.append("Failed")
                #sts_200=1
            #else:                
                #sts_200mV.append("Passed")    
        FE_res_200mv.append(sts_200mV)
        if (sts_200==1):
            Ch_res_200.append("2")
            Ch_res_200_str.append("D")
        else:
            Ch_res_200.append("1")
            Ch_res_200_str.append("A")
        if (sts_200==1):
            Failed_chs_res_chip.append(FE_chip_no)
        if (sts_200==1):
           Failed_chs_res_chip_ext.append(FE_chip_no)
        else:
           Failed_chs_res_chip_ext.append('')            
            
    else:
        print ("Measuremnets data related to channel response is not available : Ch#" + str(chip_no))

heading=["200mV BL", "SEDC OFF"]   
rows=zip(*FE_res_200mv) 
with open(file_table_chresp_ext, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()



labels = chip_list
x_pos = np.arange(len(labels))
y_pos=["Alive", "Dead"]
mean_y  = [(float(i)) for i in Ch_res_200]
error_y = [(float(i)) for i in Ch_res_200]
fig, ax = plt.subplots()
#ax.bar(x_pos, mean_y,
       #yerr=0,
       #align='center',
       #alpha=0.5,
       #ecolor='black',
       #capsize=2)
ax.set_ylabel('Channel Response (Alive/Dead)')
ax.set_xlabel(x_label_dis)
ax.set_ylim(0, 3)
#ax.set_yticks(y_pos)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, rotation='vertical', fontsize=fontsize_no)
ax.set_title('Dt:' + Date_today + '\n Channel Response Ext, 200mV BL, SEDC=OFF, A=Alive, D=Dead')
ax.yaxis.grid(True)
#for i in range(len(x_pos)):
    #plt.annotate(str(Ch_res_200_str[i]), xy=(x_pos[i], mean_y[i]), ha='center', va='bottom')
#plt.tight_layout()
#plt.savefig(root_path_plot + 'Channel_Response_200mV_Ext.png')
plt.close()

rows=zip(Failed_chs_res_chip) 
with open(file_table_failed_chip, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()


#rows=zip(Failed_chs_res_chip) 
#with open(file_table_failed_chip_detail, 'a', newline='') as csvfile:
#    csvwriter = csv.writer(csvfile)
#    for row in rows:
#        csvwriter.writerow(row)
#    csvwriter.writerow("")    
#csvfile.close()

FE_res_200mv=[]
FE_res_200mv.append(Failed_chs_res_chip_200)
FE_res_200mv.append(Failed_chs_res_chip_900)
FE_res_200mv.append(Failed_chs_res_chip_sddon)
FE_res_200mv.append(Failed_chs_res_chip_ext)

rows=zip(*FE_res_200mv) 
with open(file_table_failed_chip_detail, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")    
csvfile.close()

#part of the code added
inl_200=[]
inl_col0=[]
inl_col0.append("Ch#/Chip#")
for i in range (16):
    inl_col0.append(str(i))
inl_col0.append("Mean")
inl_col0.append("SD")

inl_200_0us=[]
inl_200_1us=[]
inl_200_2us=[]
inl_200_3us=[]

inl_200.append(inl_col0)
inl_200_0us.append(inl_col0)
inl_200_1us.append(inl_col0)
inl_200_2us.append(inl_col0)
inl_200_3us.append(inl_col0)

gain_200=[]
gain_col0=[]
gain_col0.append("Ch#/Chip#")
for i in range (16):
    gain_col0.append(str(i))
gain_col0.append("Mean")
gain_col0.append("SD")
#print(gain_col0)
gain_200.append(gain_col0)

for chip_no in chip_list_l0:
    chip_id.append(chip_no)
    FE_chip_no=str(chip_no)

    FE_chip_id=FE_chip_dis + FE_chip_no

    chip_rawdir = root_path + "Board_" + board_ID + "_"  + FE_chip_id  + "_" +  temperature + "/"
    if os.path.exists(chip_rawdir):
        pass
    else:
        try:
            os.makedirs(chip_rawdir)
        except OSError:
            print ("Error to create folder ")
            sys.exit()

    para_rawdir = chip_rawdir + "Gainmeas_acq_Cap/"
    if os.path.exists(para_rawdir):
        pass
        inl_rawdir = para_rawdir  +  FE_chip_id + "_" + Cd + "/results/"
        if os.path.exists(inl_rawdir):
            pass

        file_csv = inl_rawdir+"Gain_Lin_raw_200mV" + ".csv"

        temp=[]
        temp1=[]
        temp2=[]
        temp3=[]
        temp.append(FE_chip_no)
        temp1.append(FE_chip_no)
        temp2.append(FE_chip_no)
        temp3.append(FE_chip_no)
        for i in range(18):
            temp.append(read_cell(1, i+21, file_csv))
            temp1.append(read_cell(2, i+21, file_csv))
            temp2.append(read_cell(3, i+21, file_csv))
            temp3.append(read_cell(4, i+21, file_csv))
        inl_200.append(temp)
        inl_200_1us.append(temp1)
        inl_200_2us.append(temp2)
        inl_200_3us.append(temp3)

        temp1=[]
        temp1.append(FE_chip_no)
        for i in range(18):
            temp1.append(read_cell(2, i+1, file_csv))
        gain_200.append(temp1)


heading=["Inl Measurements", "200mV BL", "0.5us"]
rows=zip(*inl_200)
with open(file_table_inl, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

#added
heading=["Inl Measurements", "200mV BL", "1us"]
rows=zip(*inl_200_1us)
with open(file_table_inl, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

heading=["Inl Measurements", "200mV BL", "2us"]
rows=zip(*inl_200_2us)
with open(file_table_inl, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

heading=["Inl Measurements", "200mV BL", "3us"]
rows=zip(*inl_200_3us)
with open(file_table_inl, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

heading=["gain Measurements", "200mV BL"]
rows=zip(*gain_200)
with open(file_table_gain, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

inl_900=[]
inl_col0=[]
inl_col0.append("Ch#/Chip#")
for i in range (16):
    inl_col0.append(str(i))
inl_col0.append("Mean")
inl_col0.append("SD")
#print(inl_col0)

inl_900_1us=[]
inl_900_2us=[]
inl_900_3us=[]

inl_900.append(inl_col0)
inl_900_1us.append(inl_col0)
inl_900_2us.append(inl_col0)
inl_900_3us.append(inl_col0)

gain_900=[]
gain_col0=[]
gain_col0.append("Ch#/Chip#")
for i in range (16):
    gain_col0.append(str(i))
gain_col0.append("Mean")
gain_col0.append("SD")
#print(gain_col0)
gain_900.append(gain_col0)

for chip_no in chip_list_l0:
    chip_id.append(chip_no)
    FE_chip_no=str(chip_no)

    FE_chip_id=FE_chip_dis + FE_chip_no

    chip_rawdir = root_path + "Board_" + board_ID + "_"  + FE_chip_id  + "_" +  temperature + "/"
    if os.path.exists(chip_rawdir):
        pass
    else:
        try:
            os.makedirs(chip_rawdir)
        except OSError:
             print ("Error to create folder ")
             sys.exit()

    para_rawdir = chip_rawdir + "Gainmeas_acq_Cap/"
    if os.path.exists(para_rawdir):
        pass
        inl_rawdir = para_rawdir  +  FE_chip_id + "_" + Cd + "/results/"
        if os.path.exists(inl_rawdir):
            pass

        file_csv = inl_rawdir+"Gain_Lin_raw_900mV" + ".csv"

        temp=[]
        temp1=[]
        temp2=[]
        temp3=[]
        temp.append(FE_chip_no)
        temp1.append(FE_chip_no)
        temp2.append(FE_chip_no)
        temp3.append(FE_chip_no)
        for i in range(18):
            temp.append(read_cell(1, i+21, file_csv))
            temp1.append(read_cell(2, i+21, file_csv))
            temp2.append(read_cell(3, i+21, file_csv))
            temp3.append(read_cell(4, i+21, file_csv))
        inl_900.append(temp)
        inl_900_1us.append(temp1)
        inl_900_2us.append(temp2)
        inl_900_3us.append(temp3)

        temp1=[]
        temp1.append(FE_chip_no)
        for i in range(18):
            temp1.append(read_cell(2, i+1, file_csv))
        gain_900.append(temp1)

heading=["Inl Measurements", "900mV BL", "0.5us"]
rows=zip(*inl_900)
with open(file_table_inl, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

heading=["Inl Measurements", "900mV BL", "1us"]
rows=zip(*inl_900_1us)
with open(file_table_inl, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

heading=["Inl Measurements", "900mV BL", "2us"]
rows=zip(*inl_900_2us)
with open(file_table_inl, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

heading=["Inl Measurements", "900mV BL", "3us"]
rows=zip(*inl_900_3us)
with open(file_table_inl, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
csvfile.close()

heading=["gain Measurements", "900mV BL"]
rows=zip(*gain_900)
with open(file_table_gain, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    for row in rows:
        csvwriter.writerow(row)
    csvwriter.writerow("")
