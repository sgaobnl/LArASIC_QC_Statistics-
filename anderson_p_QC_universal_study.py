import os
import csv
import numpy
import random

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# flattening out lists will be useful, so we have a function defined for it
def flatten(l, ltypes=(list, tuple)):
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)

# a function to check if a string is a substring in a list of strings will be useful
def str_list(l, test):
    indicator = 0
    threshold = len(l)
    for string in l:
        if test in string:
            return True
        else:
            indicator += 1
    if indicator == threshold:
        return False

def bi_gaussian_bounds(mean, std, test_value):
    if mean - 3*std < test_value < mean + 3*std:
        return True
    else:
        return False

def upper_gaussian_bound(mean, std, test_value):
    if test_value < mean + 3*std:
        return True
    else:
        return False

# the below function tackles taking the raw batch and chip ID in the directory name and normalizing it; though the code is here
def batch_chip_processing(bcstring):
    batch_number_unprocessed = ''
    batch_number_processed = ''
    chip_id_unprocessed = ''
    chip_id_processed = ''
    # this if statement is needed to ensure the batch and chip id string is actually a number
    if bcstring.isdigit():
        # this if statement handles the case if there are less than 5 numbers in the index, which only happens for batch 000
        if len(bcstring) < 5:
            batch_number_processed = '000'
            chip_id_unprocessed = bcstring
        # this if statement handles the possibility that there are 5 digits in the raw batch/chip ID; If the value is < 10,000, it is batch 000; if it is > 9,999, the first digit is the batch # and the last 4 are the chip ID
        elif len(bcstring) == 5:
            if int(bcstring) <= 9999:
                batch_number_processed = '000'
                chip_id_unprocessed = bcstring
            else:
                batch_number_processed = f'00{bcstring[0]}0'
                chip_id_unprocessed = bcstring[1:]
        # this if statement handles the case when there are three 0's at the start of the index, which should only ever occur for batch 000
        elif '000' in bcstring[:3]:
            batch_number_processed = '000'
            chip_id_unprocessed = bcstring.lstrip(batch_number_processed)
        else:
            # this for statement deals with the remaining batches
            for char_index, char in enumerate(bcstring):
                # the batch_number_unprocessed will only ever really be used to help get the chip_id_unprocessed
                batch_number_unprocessed += char
                y = int(char)
                if y > 0:
                    batch_number_processed = f'00{bcstring[char_index]}{bcstring[char_index + 1]}'
                    # for this case, when stripping away the batch_number_unprocessed from the raw string to get the chip_id_unprocessed, it is imperative to also strip the next character as well, as that is the second 1, which is also part of the batch number
                    chip_id_unprocessed = bcstring.lstrip(bcstring[:char_index + 1])
                    # this if statement tackles the batch 0011 (1.1), since there should be no opportunity for a 1 to appear right after the first 1 unless the chip is in batch 0011; this is the general principal that should be used for subbatches (e.g. batch 2.5)
                    break
    else:
        # in the event the batch/chip ID is not a number (contains letters), return an integer value that can be used to treat exceptions
        return [-1, 0]
    # the rest of the function is dedicated to normalizing the chip ID's into 5-digit values
    deficiency_length = 5 - len(chip_id_unprocessed)
    chip_id_processed = '0'*deficiency_length + chip_id_unprocessed
    return [batch_number_processed, chip_id_processed]

def power_measurement(file_path):
    with open(file_path, 'r', newline='') as csv_file:
        data = [x for x in list(csv.reader(csv_file, delimiter=',')) if x]
    splitting_indices = []
    for index, row in enumerate(data):
        if str_list(row, 'SE'):
                splitting_indices.append(index)
    mean_values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    for splitting_index in splitting_indices:
        if str_list(data[splitting_index], '900'):
            if str_list(data[splitting_index], 'SE=OFF'):
                if str_list(data[splitting_index], 'SEDC=OFF'):
                    for row in data[splitting_index:]:
                        if str_list(row, 'Power') and str_list(row, '(mW/Ch)'):
                            for column in row:
                                if isfloat(column):
                                    mean_values[0] = float(column)
                                    break
                            break
                elif str_list(data[splitting_index], 'SEDC=ON'):
                    for row in data[splitting_index:]:
                        if str_list(row, 'Power') and str_list(row, '(mW/Ch)'):
                            for column in row:
                                if isfloat(column):
                                    mean_values[2] = float(column)
                                    break
                            break
            elif str_list(data[splitting_index], 'SE=ON') and str_list(data[splitting_index], 'SEDC=OFF'):
                for row in data[splitting_index:]:
                    if str_list(row, 'Power') and str_list(row, '(mW/Ch)'):
                        for column in row:
                            if isfloat(column):
                                mean_values[1] = float(column)
                                break
                        break
        elif str_list(data[splitting_index], '200'):
            if str_list(data[splitting_index], 'SE=OFF'):
                if str_list(data[splitting_index], 'SEDC=OFF'):
                    for row in data[splitting_index:]:
                        if str_list(row, 'Power') and str_list(row, '(mW/Ch)'):
                            for column in row:
                                if isfloat(column):
                                    mean_values[3] = float(column)
                                    break
                            break
                elif str_list(data[splitting_index], 'SEDC=ON'):
                    for row in data[splitting_index:]:
                        if str_list(row, 'Power') and str_list(row, '(mW/Ch)'):
                            for column in row:
                                if isfloat(column):
                                    mean_values[5] = float(column)
                                    break
                            break
            elif str_list(data[splitting_index], 'SE=ON') and str_list(data[splitting_index], 'SEDC=OFF'):
                for row in data[splitting_index:]:
                    if str_list(row, 'Power') and str_list(row, '(mW/Ch)'):
                        for column in row:
                            if isfloat(column):
                                mean_values[4] = float(column)
                                break
                        break
    return mean_values

def fe_parameter(file_path):
    indicator = 0
    channel_data = [[]]*16
    with open(file_path, 'r', newline='') as csv_file:
        data = [x for x in list(csv.reader(csv_file, delimiter=',')) if x != []]
    for i in reversed(data):
        if 'SD' in i[0]:
            sd_data = [float(x) for x in i[1:]]
        elif 'Mean' in i[0]:
            mean_data = [float(x) for x in i[1:]]
        elif i[0].isdigit():
            channel_data[int(i[0])] = [float(x) for x in i[1:]]
            if int(i[0]) == 0:
                break
    for k in range(0, len(mean_data)):
        for p in range(0, 16):
            if bi_gaussian_bounds(mean_data[k], sd_data[k], channel_data[p][k]):
                indicator += 1
            else:
                break
    if indicator == 32:
        return flatten(['Passed', mean_data])
    else:
        return ['Failed', 0.0, 0.0]

def channel_resp_sedc_off(file_path):
    with open(file_path, 'r', newline='') as csv_file:
        data = [x for x in list(csv.reader(csv_file, delimiter=',')) if x]
    splitting_indices = [0, 0]
    for indx, row in enumerate(data):
        if '900' in row[0] and 'SEDC=OFF' in row[1]:
            splitting_indices[1] = indx
        elif '200' in row[0] and 'SEDC=OFF' in row[1]:
            splitting_indices[0] = indx
    if flatten(data[splitting_indices[0]:splitting_indices[1]]).count('Passed') == 64 and flatten(data[splitting_indices[1]:]).count('Passed') == 64:
        return ['Passed']
    else:
        return ['Failed']

def channel_resp_sedc_on(file_path):
    with open(file_path, 'r', newline='') as csv_file:
        data = [x for x in list(csv.reader(csv_file, delimiter=',')) if x]
    splitting_indices = [0]
    for indx, row in enumerate(data):
        if '200' in data[0] and 'SEDC=ON' in data[1]:
            splitting_indices[0] = indx
    if flatten(data[splitting_indices[0]:]).count('Passed') == 16:
        return ['Passed']
    else:
        return ['Failed']

def ext_pulse(file_path):
    with open(file_path, 'r', newline='') as csv_file:
        data = [x for x in list(csv.reader(csv_file, delimiter=',')) if x]
    splitting_indices = [0]
    for indx, row in enumerate(data):
        if '200' in row[0] and 'SEDC=OFF' in row[1]:
            splitting_indices[0] = indx
    if flatten(data[splitting_indices[0]:]).count('Passed') == 16:
        return ['Passed']
    else:
        return ['Failed']

def bl_restore(file_path):
    with open(file_path, 'r', newline='') as csv_file:
        data = [x for x in list(csv.reader(csv_file, delimiter=',')) if x]
    splitting_indices = [0]
    for indx, row in enumerate(data):
        if 'Ch' in row[0]:
            splitting_indices[0] = indx
    if flatten(data[splitting_indices[0]:]).count('Passed') == 32:
        return ['Passed']
    else:
        return ['Failed']

def power_cycle(file_path):
    with open(file_path, 'r', newline='') as csv_file:
        data = [x for x in list(csv.reader(csv_file, delimiter=',')) if x]
    splitting_indices = [0]
    for indx, row in enumerate(data):
        if '200' in data[0] and 'SEDC=OFF' in data[1]:
            splitting_indices[0] = indx
    if flatten(data[splitting_indices[0]:]).count('Passed') == 48:
        return ['Passed']
    else:
        return ['Failed']

def gain_plot_200(file_path):
    indicator_Gain = 0
    indicator_INL = 0
    channel_data_Gain = []
    channel_data_INL = [[]] * 16
    with open(file_path, 'r', newline='') as csv_file:
        data = [x for x in list(csv.reader(csv_file, delimiter=',')) if x]
    splitting_indices = [0, 0]
    for indx, row in enumerate(data):
        if str_list(row, 'Gain'):
            splitting_indices[0] = indx
        elif str_list(row, 'INL'):
            splitting_indices[1] = indx
    # this next chunk handles the Gain
    for i in data[splitting_indices[0]:]:
        if i[0].isdigit():
            if int(i[0]) == 0:
                channel_0_data = [float(x) for x in i[1:]]
            elif int(i[0]) == 8:
                channel_8_data = [float(x) for x in i[1:]]
            else:
                channel_data_Gain.append([float(x) for x in i[1:]])
        if 'Mean' in i[0]:
            mean_data_Gain = [float(x) for x in i[1:]]
        elif 'SD' in i[0]:
            sd_data_Gain = [float(x) for x in i[1:]]
            break
    # this next chunk handles the INL
    for i in data[splitting_indices[1]:]:
        if i[0].isdigit():
            channel_data_INL[int(i[0])] = [float(x) for x in i[1:]]
        if 'Mean' in i[0]:
            mean_data_INL = [float(x) for x in i[1:]]
        elif 'SD' in i[0]:
            sd_data_INL = [float(x) for x in i[1:]]
            break
    # this next chunk handles checking each channel for Gain
    for k in range(0, len(mean_data_Gain)):
        for p in range(0, 14):
            if bi_gaussian_bounds(mean_data_Gain[k], sd_data_Gain[k], channel_data_Gain[p][k]):
                indicator_Gain += 1
            else:
                break
    # this next chunk handles checking each channel for INL
    for k in range(0, len(mean_data_INL)):
        for j in range(0, 16):
            if upper_gaussian_bound(mean_data_INL[k], sd_data_INL[k], channel_data_INL[j][k]) and channel_data_INL[j][k] < 1:
                indicator_INL += 1
            else:
                break
    if indicator_Gain == 56 and indicator_INL == 64:
        return flatten(['Passed', mean_data_Gain, mean_data_INL, channel_0_data, channel_8_data])
    else:
        return ['Failed', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def gain_plot_900(file_path):
    indicator_Gain = 0
    indicator_INL = 0
    channel_data_Gain = []
    channel_data_INL = [[]] * 16
    with open(file_path, 'r', newline='') as csv_file:
        data = [x for x in list(csv.reader(csv_file, delimiter=',')) if x]
    splitting_indices = [0, 0]
    for indx, row in enumerate(data):
        if str_list(row, 'Gain'):
            splitting_indices[0] = indx
        elif str_list(row, 'INL'):
            splitting_indices[1] = indx
    # this next chunk handles the Gain
    for i in data[splitting_indices[0]:]:
        if i[0].isdigit():
            if int(i[0]) == 0:
                channel_0_data = [float(x) for x in i[1:]]
            elif int(i[0]) == 8:
                channel_8_data = [float(x) for x in i[1:]]
            else:
                channel_data_Gain.append([float(x) for x in i[1:]])
        if 'Mean' in i[0]:
            mean_data_Gain = [float(x) for x in i[1:]]
        elif 'SD' in i[0]:
            sd_data_Gain = [float(x) for x in i[1:]]
            break
    # this next chunk handles the INL
    for i in data[splitting_indices[1]:]:
        if i[0].isdigit():
            channel_data_INL[int(i[0])] = [float(x) for x in i[1:]]
        if 'Mean' in i[0]:
            mean_data_INL = [float(x) for x in i[1:]]
        elif 'SD' in i[0]:
            sd_data_INL = [float(x) for x in i[1:]]
            break
    # this next chunk handles checking each channel for Gain
    for k in range(0, len(mean_data_Gain)):
        for p in range(0, 14):
            # the normal constraint of using 3 standard deviations seems to be too high, so we just replace it with +- 2
            if bi_gaussian_bounds(mean_data_Gain[k], sd_data_Gain[k], channel_data_Gain[p][k]):
                indicator_Gain += 1
            else:
                break
    # this next chunk handles checking each channel for INL
    for k in range(0, len(mean_data_INL)):
        for j in range(0, 16):
            if upper_gaussian_bound(mean_data_INL[k], sd_data_INL[k], channel_data_INL[j][k]) and channel_data_INL[j][k] < 1:
                indicator_INL += 1
            else:
                break
    if indicator_Gain == 56 and indicator_INL == 64:
        return flatten(['Passed', mean_data_Gain, mean_data_INL, channel_0_data, channel_8_data])
    else:
        return ['Failed', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def noise_measurement(file_path):
    indicator = 0
    num_cols = 4
    threshold = num_cols * 16
    channel_data = [[]]*16
    with open(file_path, 'r', newline='') as csv_file:
        data = [x for x in list(csv.reader(csv_file, delimiter=',')) if x]
    for i in reversed(data):
        if 'SD' in i[0]:
            sd_data = [float(x) for x in i[1:]]
        elif 'Mean' in i[0]:
            mean_data = [float(x) for x in i[1:]]
        elif i[0].isdigit():
            channel_data[int(i[0])] = [float(x) for x in i[1:]]
            if int(i[0]) == 0:
                break
    for k in range(0, len(mean_data)):
        for p in range(0, 16):
            if upper_gaussian_bound(mean_data[k], sd_data[k], channel_data[p][k]):
                indicator += 1
            else:
                break
    if indicator == threshold:
        return flatten(['Passed', mean_data])
    else:
        return ['Failed', 0.0, 0.0, 0.0, 0.0]

def test_data_processing(file_path, file_name, raw_batch_chip):
    test_funct_dict = {f'Power_FEChip_P5B_{raw_batch_chip}.csv' : [0, power_measurement],
                        f'Baseline_VBGR_Temp_FEChip_P5B_{raw_batch_chip}.csv' : [1, fe_parameter],
                        'Channel_Response_result_DACpls_900mV_200mV_SEDC_OFF.csv': [2, channel_resp_sedc_off],
                        'Channel_Response_result_DACpls_200mV_SEDC_ON.csv' : [3, channel_resp_sedc_on],
                        'Channel_Response_result_Extpls_200mV_SEDC_OFF.csv' : [4, ext_pulse],
                        'Channel_BL_restore_test.csv': [5, bl_restore],
                        'Power_Cycle_Channel_Response_result_DACpls_900mV_200mV_SEDC_OFF.csv': [6, power_cycle],
                        'Gain_Lin_raw_200mV.csv' : [7, gain_plot_200],
                        'Gain_Lin_raw_900mV.csv' : [8, gain_plot_900],
                        'Noise_ENC_raw.csv': [9, noise_measurement]
    }
    if file_name in test_funct_dict:
        return [test_funct_dict[file_name][0], test_funct_dict[file_name][1](file_path)]
    else:
        return 'No File Found'

# this table associates each test type to the position in the test_data list where their associated information starts being inserted
data_positions = [5, 11, 14, 15, 16, 17, 18, 19, 36, 53]

# change Current Working Directory (CWD), the directory that will be scanned as needed
os.chdir('Y:')

# this directory is where data files compiling the results of this program will be distributed
output_directory = r'C:\Paul'

# This next list accumulates the batch numbers being worked with
batch_numbers = []

# this next variable cuts the number of lines of code in about half
test_env = ['RT','LN']

# this batch catalogs the directories that did not conform to the naming standard we are using
bad_directory_names = []

# after the first os.walk, it will be useful to catalog all the relevant test directories, those that conform to our naming standards, so their path strings are collected in this list
test_dir_paths = []

# in the event data scans are done more than once, it's efficient to not rescan folders that have already been scanned. Thus, test_sup_dir_paths_new will tag folders in the current run that have been scanned, so they aren't scanned in future runs
test_sup_dir_paths_new = []

# this list will list all directories just below LArASIC_QC that have already been checked, and so can be skipped in future runs, saving time
test_sup_dir_paths_old = []

# this next chunk of code deals with possibility of previous directories already being scanned, and so being skippable
if os.path.exists(os.path.join(output_directory, 'testSupDirs.csv')):
    # this if statement speeds up analysis in the event some directories have already been analyzed; any such folders would be written in the testSupDirs.csv file
    with open(os.path.join(output_directory, 'testSupDirs.csv'), 'r', newline='') as csv_file:
        test_sup_dir_paths_old = flatten(list(csv.reader(csv_file, delimiter=',')))
else:
    test_sup_dir_paths_old = []

# this line identifies the new directories LArASIC_QC
test_sup_dir_paths_new = [d for d in os.listdir(r'.\LArASIC_QC') if d not in test_sup_dir_paths_old]

# this next if statement tracks all the actual test directories, and ensures it's not a subdirectory
for dir, subdirs, files in os.walk('.', topdown=True):
    subdirs[:] = [d for d in subdirs if d not in test_sup_dir_paths_old]
    if 'DUAL_DUT_FEChip' in dir and '\\' not in dir.split('DUAL_DUT_FEChip')[1]:
        test_dir_paths.append(dir)
        subdirs.clear()

# Now it is time to make the data tables
for test_dir_path in test_dir_paths:
    # this list will contain the information we need for data analysis
    test_data = [[]]*102
    # This next section tackles the processing of batch number and chip ID
    test_dir_name = test_dir_path.split('_')
    # Use FEChip as a reference point to find raw batch and chip ID
    fe_chip_reference = test_dir_name.index('FEChip')
    batch_chip_id_raw = test_dir_name[fe_chip_reference + 2]
    # process the raw batch number and chip ID
    try:
        test_data[0:2] = batch_chip_processing(batch_chip_id_raw)
    except (ValueError, IndexError):
        bad_directory_names.append(test_dir_path)
        continue
    if test_data[0] == -1:
        bad_directory_names.append(test_dir_path)
        continue
    # append the raw batch number and chip ID
    test_data[2] = batch_chip_id_raw
    # this next line also accounts for the testing environment being either RT or LN
    test_data[3] = test_dir_name[fe_chip_reference + 3]
    # list the directory path
    test_data[4] = test_dir_path

    # from here, it's a matter of reading the test result files, but we first need to find them; for that, we use another os.walk
    for dir_path, test_subdir, test_filenames in os.walk(test_dir_path, topdown=True):
        for test_filename in test_filenames:
            single_test_output = test_data_processing(os.path.join(dir_path, test_filename), test_filename, batch_chip_id_raw)
            if single_test_output == 'No File Found':
                continue
            else:
                for ind, data_position in enumerate(data_positions):
                    if ind == single_test_output[0]:
                        test_data[data_position:data_position + len(single_test_output[1])] = single_test_output[1]
    # this last section apportions the final data according to the batch the test data was from
    if test_data.count('Passed') + test_data.count('Failed') < 9:
        continue
    elif f'data_table_{test_data[0]}_{test_data[3]}' in globals():
        globals()[f'data_table_{test_data[0]}_{test_data[3]}'].append(test_data)
    else:
        globals()[f'data_table_{test_data[0]}_{test_data[3]}'] = [test_data]
        batch_numbers.append(test_data[0])

batch_numbers = list(set(batch_numbers))
if '000' in batch_numbers:
    batch_numbers.remove('000')
if '0099' in batch_numbers:
    batch_numbers.remove('0099')

# this chunk handles writing out the data tables into .csv files
for l in test_env:
    for i in batch_numbers:
        # need to make sure the data table actually exists, specifically since some chips might not have been tested in LN
        if f'data_table_{i}_{l}' in globals():
            if os.path.exists(os.path.join(output_directory, f'data_table_{i}_{l}.csv')):
                with open(os.path.join(output_directory, f'data_table_{i}_{l}.csv'), 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(globals()[f'data_table_{i}_{l}'])
            else:
                with open(os.path.join(output_directory, f'data_table_{i}_{l}.csv'), 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(globals()[f'data_table_{i}_{l}'])

# we create labels for the stat_bounds files
universal_data_labels = ['Power Measurement SE=OFF SEDC=OFF 900mV mean', 'Power Measurement SE=ON SEDC=OFF 900mV mean', 'Power Measurement SE=OFF SEDC=ON 900mV mean',
                    'Power Measurement SE=OFF SEDC=OFF 200mV mean', 'Power Measurement SE=ON SEDC=OFF 200mV mean', 'Power Measurement SE=OFF SEDC=ON 200mV mean',
                    'Power Measurement SE=OFF SEDC=OFF 900mV std', 'Power Measurement SE=ON SEDC=OFF 900mV std', 'Power Measurement SE=OFF SEDC=ON 900mV std',
                    'Power Measurement SE=OFF SEDC=OFF 200mV std', 'Power Measurement SE=ON SEDC=OFF 200mV std', 'Power Measurement SE=OFF SEDC=ON 200mV std',
                    'FE Parameter 200mV mean', 'FE Parameter 900mV mean', 'FE Parameter 200mV std', 'FE Parameter 900mV std',
                    'FE gain plot 200mV mean gain @0.5', 'FE gain plot 200mV mean gain @1', 'FE gain plot 200mV mean gain @2', 'FE gain plot 200mV mean gain @3',
                    'FE gain plot 200mV mean INL @0.5', 'FE gain plot 200mV mean INL @1', 'FE gain plot 200mV mean INL @2', 'FE gain plot 200mV mean INL @3',
                    'FE gain plot 200mV std gain @0.5', 'FE gain plot 200mV std gain @1', 'FE gain plot 200mV std gain @2', 'FE gain plot 200mV std gain @3',
                    'FE gain plot 200mV std INL @0.5', 'FE gain plot 200mV std INL @1', 'FE gain plot 200mV td INL @2', 'FE gain plot 200mV std INL @3',
                    'FE gain plot 900mV mean gain @0.5', 'FE gain plot 900mV mean gain @1', 'FE gain plot 900mV mean gain @2', 'FE gain plot 900mV mean gain @3',
                    'FE gain plot 900mV mean INL @0.5', 'FE gain plot 900mV mean INL @1', 'FE gain plot 900mV mean INL @2', 'FE gain plot 900mV mean INL @3',
                    'FE gain plot 900mV std gain @0.5', 'FE gain plot 900mV std gain @1', 'FE gain plot 900mV std gain @2', 'FE gain plot 900mV std gain @3',
                    'FE gain plot 900mV std INL @0.5', 'FE gain plot 900mV std INL @1', 'FE gain plot 900mV td INL @2', 'FE gain plot 900mV std INL @3',
                    'FE Noise ENC mean @0.5', 'FE Noise ENC mean @1', 'FE Noise ENC mean @2', 'FE Noise ENC mean @3',
                    'FE Noise ENC std @0.5', 'FE Noise ENC std @1', 'FE Noise ENC std @2', 'FE Noise ENC std @3',
                    'channel 0 gain 200mV mean @0.5', 'channel 0 gain 200mV mean @1', 'channel 0 gain 200mV mean @2', 'channel 0 gain 200mV mean @3',
                    'channel 8 gain 200mV mean @0.5', 'channel 8 gain 200mV mean @1', 'channel 8 gain 200mV mean @2', 'channel 8 gain 200mV mean @3',
                    'channel 0 gain 200mV std @0.5', 'channel 0 gain 200mV std @1', 'channel 0 gain 200mV std @2', 'channel 0 gain 200mV std @3',
                    'channel 8 gain 200mV std @0.5', 'channel 8 gain 200mV std @1', 'channel 8 gain 200mV std @2', 'channel 8 gain 200mV std @3',
                    'channel 0 gain 900mV mean @0.5', 'channel 0 gain 900mV mean @1', 'channel 0 gain 900mV mean @2', 'channel 0 gain 900mV mean @3',
                    'channel 8 gain 900mV mean @0.5', 'channel 8 gain 900mV mean @1', 'channel 8 gain 900mV mean @2', 'channel 8 gain 900mV mean @3',
                    'channel 0 gain 900mV std @0.5', 'channel 0 gain 900mV std @1', 'channel 0 gain 900mV std @2', 'channel 0 gain 900mV std @3',
                    'channel 8 gain 900mV std @0.5', 'channel 8 gain 900mV std @1', 'channel 8 gain 900mV std @2', 'channel 8 gain 900mV std @3']


# this chunk of code handles generating the statistical bounds used for the universal study, or reading them off if they're already created
for l in test_env:
    for i in batch_numbers:
        if os.path.exists(os.path.join(output_directory, f'universal_data_sample_{i}_{l}.csv')):
            # if the stat bounds have already been written into a file, they are just read off from the .csv files
            if os.path.exists(os.path.join(output_directory, f'stat_bounds_{i}_{l}.csv')):
                with open(os.path.join(output_directory, f'stat_bounds_{i}_{l}.csv'), 'r', newline='') as csv_file:
                    globals()[f'universal_data_{i}_{l}'] = [float(x) for x in list(zip(*list(csv.reader(csv_file, delimiter=','))))[1]]
                    continue
            else:
                with open(os.path.join(output_directory, f'universal_data_sample_{i}_{l}.csv'), 'r', newline='') as csv_file:
                    universal_data_sample = list(csv.reader(csv_file, delimiter=','))

                universal_data_sample_transpose = list(zip(*universal_data_sample))

                # Power Measurement
                channel_data = numpy.array(universal_data_sample_transpose[5:11], dtype=float)
                globals()[f'universal_data_{i}_{l}'][0:6] = numpy.mean(channel_data, axis=1)
                globals()[f'universal_data_{i}_{l}'][6:12] = numpy.std(channel_data, axis=1)

                # FE Parameter
                channel_data = numpy.array(universal_data_sample_transpose[12:14], dtype=float)
                globals()[f'universal_data_{i}_{l}'][12:14] = numpy.mean(channel_data, axis=1)
                globals()[f'universal_data_{i}_{l}'][14:16] = numpy.std(channel_data, axis=1)

                # Gain plot 200mV gain and INL (most channels)
                channel_data = numpy.array(universal_data_sample_transpose[20:28], dtype=float)
                globals()[f'universal_data_{i}_{l}'][16:24] = numpy.mean(channel_data, axis=1)
                globals()[f'universal_data_{i}_{l}'][24:32] = numpy.std(channel_data, axis=1)

                # Gain plot 900mV gain and INL (most channels)
                channel_data = numpy.array(universal_data_sample_transpose[37:45], dtype=float)
                globals()[f'universal_data_{i}_{l}'][32:40] = numpy.mean(channel_data, axis=1)
                globals()[f'universal_data_{i}_{l}'][40:48] = numpy.std(channel_data, axis=1)

                # FE Noise ENC (if future tests are incorporated, [38:] will need to be updated
                channel_data = numpy.array(universal_data_sample_transpose[54:58], dtype=float)
                globals()[f'universal_data_{i}_{l}'][48:52] = numpy.mean(channel_data, axis=1)
                globals()[f'universal_data_{i}_{l}'][52:56] = numpy.std(channel_data, axis=1)

                # Gain plot 200mV gain (channels 0 and 8)
                channel_data = numpy.array(universal_data_sample_transpose[28:36], dtype=float)
                globals()[f'universal_data_{i}_{l}'][56:64] = numpy.mean(channel_data, axis=1)
                globals()[f'universal_data_{i}_{l}'][64:72] = numpy.std(channel_data, axis=1)

                # Gain plot 900mV gain (channels 0 and 8)
                channel_data = numpy.array(universal_data_sample_transpose[45:53], dtype=float)
                globals()[f'universal_data_{i}_{l}'][72:80] = numpy.mean(channel_data, axis=1)
                globals()[f'universal_data_{i}_{l}'][80:] = numpy.std(channel_data, axis=1)

                with open(os.path.join(output_directory, f'stat_bounds_{i}_{l}.csv'), 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(list(zip(*[universal_data_labels, globals()[f'universal_data_{i}_{l}']])))
                continue
        else:
            if f'data_table_{i}_{l}' in globals():
                globals()[f'universal_data_{i}_{l}'] = numpy.zeros(88)
                universal_data_ids = []
                universal_data_sample = []
                # sample size will need to be different depending on RT vs. LN
                if l == 'RT':
                    sample_size = 100
                elif l == 'LN':
                    sample_size = 10
                while len(universal_data_ids) < sample_size:
                    ind = random.randint(0, len(globals()[f'data_table_{i}_{l}']) - 1)
                    test_data = globals()[f'data_table_{i}_{l}'][ind]
                    if not test_data[1] in universal_data_ids:
                        if test_data[11] == 'Passed' and test_data[
                        14] == 'Passed' and test_data[15] == 'Passed' and test_data[16] == 'Passed' and test_data[
                        17] == 'Passed' and test_data[18] == 'Passed' and test_data[19] == 'Passed' and test_data[
                        36] == 'Passed' and test_data[53] == 'Passed':
                            universal_data_sample.append(test_data)
                            universal_data_ids.append(test_data[1])
                with open(os.path.join(output_directory, f'universal_data_sample_{i}_{l}.csv'), 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(universal_data_sample)

            universal_data_sample_transpose = list(zip(*universal_data_sample))

            # Power Measurement
            channel_data = numpy.array(universal_data_sample_transpose[5:11], dtype=float)
            globals()[f'universal_data_{i}_{l}'][0:6] = numpy.mean(channel_data, axis=1)
            globals()[f'universal_data_{i}_{l}'][6:12] = numpy.std(channel_data, axis=1)

            # FE Parameter
            channel_data = numpy.array(universal_data_sample_transpose[12:14], dtype=float)
            globals()[f'universal_data_{i}_{l}'][12:14] = numpy.mean(channel_data, axis=1)
            globals()[f'universal_data_{i}_{l}'][14:16] = numpy.std(channel_data, axis=1)

            # Gain plot 200mV gain and INL (most channels)
            channel_data = numpy.array(universal_data_sample_transpose[20:28], dtype=float)
            globals()[f'universal_data_{i}_{l}'][16:24] = numpy.mean(channel_data, axis=1)
            globals()[f'universal_data_{i}_{l}'][24:32] = numpy.std(channel_data, axis=1)

            # Gain plot 900mV gain and INL (most channels)
            channel_data = numpy.array(universal_data_sample_transpose[37:45], dtype=float)
            globals()[f'universal_data_{i}_{l}'][32:40] = numpy.mean(channel_data, axis=1)
            globals()[f'universal_data_{i}_{l}'][40:48] = numpy.std(channel_data, axis=1)

            # FE Noise ENC (if future tests are incorporated, [38:] will need to be updated
            channel_data = numpy.array(universal_data_sample_transpose[54:58], dtype=float)
            globals()[f'universal_data_{i}_{l}'][48:52] = numpy.mean(channel_data, axis=1)
            globals()[f'universal_data_{i}_{l}'][52:56] = numpy.std(channel_data, axis=1)

            # Gain plot 200mV gain (channels 0 and 8)
            channel_data = numpy.array(universal_data_sample_transpose[28:36], dtype=float)
            globals()[f'universal_data_{i}_{l}'][56:64] = numpy.mean(channel_data, axis=1)
            globals()[f'universal_data_{i}_{l}'][64:72] = numpy.std(channel_data, axis=1)

            # Gain plot 900mV gain (channels 0 and 8)
            channel_data = numpy.array(universal_data_sample_transpose[45:53], dtype=float)
            globals()[f'universal_data_{i}_{l}'][72:80] = numpy.mean(channel_data, axis=1)
            globals()[f'universal_data_{i}_{l}'][80:] = numpy.std(channel_data, axis=1)

            with open(os.path.join(output_directory, f'stat_bounds_{i}_{l}.csv'), 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(list(zip(*[universal_data_labels, globals()[f'universal_data_{i}_{l}']])))

# this concludes writing up the statistical data; now it's just a matter of comparing each data table's entry with their respective distribution and seeing if they lie within the desired bounds
for l in test_env:
    for i in batch_numbers:
        if f'data_table_{i}_{l}' in globals():
            for m in range(0, len(globals()[f'data_table_{i}_{l}'])):
                # Test Power Measurement
                for k in range(0, 6):
                    if bi_gaussian_bounds(globals()[f'universal_data_{i}_{l}'][k], globals()[f'universal_data_{i}_{l}'][k + 6], float(globals()[f'data_table_{i}_{l}'][m][k + 5])):
                        globals()[f'data_table_{i}_{l}'][m][58 + k] = 'Passed'
                    else:
                        globals()[f'data_table_{i}_{l}'][m][58 + k] = 'Failed'
                # Test FE Parameter
                for k in range(0, 2):
                    if bi_gaussian_bounds(globals()[f'universal_data_{i}_{l}'][12 + k], globals()[f'universal_data_{i}_{l}'][k + 14], float(globals()[f'data_table_{i}_{l}'][m][k + 12])):
                        globals()[f'data_table_{i}_{l}'][m][64 + k] = 'Passed'
                    else:
                        globals()[f'data_table_{i}_{l}'][m][64 + k] = 'Failed'
                # Test gain plot mean gain 200mV (most channels)
                for k in range(0, 4):
                    if bi_gaussian_bounds(globals()[f'universal_data_{i}_{l}'][16 + k], globals()[f'universal_data_{i}_{l}'][k + 24], float(globals()[f'data_table_{i}_{l}'][m][k + 20])):
                        globals()[f'data_table_{i}_{l}'][m][66 + k] = 'Passed'
                    else:
                        globals()[f'data_table_{i}_{l}'][m][66 + k] = 'Failed'
                # Test gain plot mean INL 200mV (most channels)
                for k in range(0, 4):
                    if upper_gaussian_bound(globals()[f'universal_data_{i}_{l}'][k + 20], globals()[f'universal_data_{i}_{l}'][k + 28], float(globals()[f'data_table_{i}_{l}'][m][k + 24])):
                        globals()[f'data_table_{i}_{l}'][m][70 + k] = 'Passed'
                    else:
                        globals()[f'data_table_{i}_{l}'][m][70 + k] = 'Failed'
                # Test gain plot mean gain 900mV (most channels)
                for k in range(0, 4):
                    if bi_gaussian_bounds(globals()[f'universal_data_{i}_{l}'][32 + k], globals()[f'universal_data_{i}_{l}'][k + 40], float(globals()[f'data_table_{i}_{l}'][m][k + 37])):
                        globals()[f'data_table_{i}_{l}'][m][74 + k] = 'Passed'
                    else:
                        globals()[f'data_table_{i}_{l}'][m][74 + k] = 'Failed'
                # Test gain plot mean INL 900mV
                for k in range(0, 4):
                    if upper_gaussian_bound(globals()[f'universal_data_{i}_{l}'][k + 36], globals()[f'universal_data_{i}_{l}'][k + 44], float(globals()[f'data_table_{i}_{l}'][m][k + 41])):
                        globals()[f'data_table_{i}_{l}'][m][78 + k] = 'Passed'
                    else:
                        globals()[f'data_table_{i}_{l}'][m][78 + k] = 'Failed'
                # Test FE Noise ENC
                for k in range(0, 4):
                    if upper_gaussian_bound(globals()[f'universal_data_{i}_{l}'][k + 48], globals()[f'universal_data_{i}_{l}'][k + 52], float(globals()[f'data_table_{i}_{l}'][m][k + 54])):
                        globals()[f'data_table_{i}_{l}'][m][82 + k] = 'Passed'
                    else:
                        globals()[f'data_table_{i}_{l}'][m][82 + k] = 'Failed'
                # Test gain plot 200mV gain (channels 0 and 8)
                for k in range(0, 8):
                    if bi_gaussian_bounds(globals()[f'universal_data_{i}_{l}'][56 + k], globals()[f'universal_data_{i}_{l}'][k + 64], float(globals()[f'data_table_{i}_{l}'][m][k + 28])):
                        globals()[f'data_table_{i}_{l}'][m][86 + k] = 'Passed'
                    else:
                        globals()[f'data_table_{i}_{l}'][m][86 + k] = 'Failed'
                # Test gain plot 900mV gain (channels 0 and 8)
                for k in range(0, 8):
                    if bi_gaussian_bounds(globals()[f'universal_data_{i}_{l}'][72 + k], globals()[f'universal_data_{i}_{l}'][k + 80], float(globals()[f'data_table_{i}_{l}'][m][k + 45])):
                        globals()[f'data_table_{i}_{l}'][m][94 + k] = 'Passed'
                    else:
                        globals()[f'data_table_{i}_{l}'][m][94 + k] = 'Failed'


# this chunk handles writing out the data tables into .csv files
for l in test_env:
    for i in batch_numbers:
        # need to make sure the data table actually exists, specifically since some chips might not have been tested in LN
        if f'data_table_{i}_{l}' in globals():
            if os.path.exists(os.path.join(output_directory, f'data_table_complete_{i}_{l}.csv')):
                with open(os.path.join(output_directory, f'data_table_complete_{i}_{l}.csv'), 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(globals()[f'data_table_{i}_{l}'])
            else:
                with open(os.path.join(output_directory, f'data_table_complete_{i}_{l}.csv'), 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(globals()[f'data_table_{i}_{l}'])

# this completes making the large data tables; however, they're frankly too large, with too much data, so we cut them down to only include final statuses of the 9 tests
for l in test_env:
    for i in batch_numbers:
        # need to make sure the data table actually exists, specifically since some chips might not have been tested in LN
        if f'data_table_{i}_{l}' in globals():
            for test_data in globals()[f'data_table_{i}_{l}']:
                test_data_reduced = test_data[0:5]
                # we now just check if each test passed or failed, starting with Power Measurement
                if test_data[58:64].count('Passed') == 6:
                    test_data_reduced.append('Passed')
                else:
                    test_data_reduced.append('Failed')
                # FE parameter
                if test_data[11] == 'Passed' and test_data[64:66].count('Passed') == 2:
                    test_data_reduced.append('Passed')
                else:
                    test_data_reduced.append('Failed')
                # Channel response SEDC=OFF, Channel response SEDC=ON, Channel response Ext Pulse, BL Restore, Power Cycle (these five could be done during the making of data_table if memory isn't an issue)
                for j in range(0, 5):
                    if test_data[14 + j] == 'Passed':
                        test_data_reduced.append('Passed')
                    else:
                        test_data_reduced.append('Failed')
                # gain plot
                if test_data[19] == 'Passed' and test_data[36] == 'Passed' and test_data[66:82].count('Passed') == 16 and test_data[86:].count('Passed') == 16:
                    test_data_reduced.append('Passed')
                else:
                    test_data_reduced.append('Failed')
                # FE noise
                if test_data[53] == 'Passed' and test_data[82:86].count('Passed') == 4:
                    test_data_reduced.append('Passed')
                else:
                    test_data_reduced.append('Failed')
                # once again, this data needs to be compiled in a data table
                if f'data_table_reduced_{i}_{l}' in globals():
                    globals()[f'data_table_reduced_{i}_{l}'].append(test_data_reduced)
                else:
                    globals()[f'data_table_reduced_{i}_{l}'] = [test_data_reduced]
            # again, we write out the data_table_reduced to a .csv file
            if os.path.exists(os.path.join(output_directory, f'data_table_reduced_{i}_{l}.csv')):
                with open(os.path.join(output_directory, f'data_table_reduced_{i}_{l}.csv'), 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerows(globals()[f'data_table_reduced_{i}_{l}'])
            else:
                with open(os.path.join(output_directory, f'data_table_reduced_{i}_{l}.csv'), 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerows(globals()[f'data_table_reduced_{i}_{l}'])

# this completes compiling the tables of test data; now we simply need to count passes and fails; the next chunk of code does that
for l in test_env:
    for i in batch_numbers:
        if f'data_table_reduced_{i}_{l}' in globals():
            globals()[f'passed_chip_{i}_{l}'] = []
            globals()[f'failed_chip_{i}_{l}'] = []
            # entries of lists that need testing are 5 - 12, with base 0 (meaning there are 8 tests to pass)
            # (1) this first round will check for all chips that pass ever test, the strongest success condition, but not the final one.
            for test_data in globals()[f'data_table_reduced_{i}_{l}']:
                pass_counter = 0
                for j in range(5, 13):
                    if test_data[j] == 'Failed':
                        break
                    else:
                        pass_counter += 1
                if pass_counter == 8:
                    globals()[f'passed_chip_{i}_{l}'].append(test_data[1])
                else:
                    globals()[f'failed_chip_{i}_{l}'].append(test_data[1])
    # we need to cut down the size of the failed bin, as some chips might have failed multiple times. We do this by converting the failed bin to a set, which removes duplicates, and then convert it back to a list.
    # we also cut down the size of the passed bin, to account for the possibility a successful chip is tested again (in the rare instance it happens)
    for i in batch_numbers:
        if f'data_table_reduced_{i}_{l}' in globals():
            globals()[f'failed_chip_{i}_{l}'] = list(set(globals()[f'failed_chip_{i}_{l}']))
            globals()[f'passed_chip_{i}_{l}'] = list(set(globals()[f'passed_chip_{i}_{l}']))
    # chips tested multiple times might appear in both the passed and failed bins. However, so long as they passed once, the failed ones are irrelevant. Thus, if we spot a chip ID in both the passed and failed bins, we can just remove it from the failed bin
    for i in batch_numbers:
        if f'data_table_reduced_{i}_{l}' in globals():
            for passed_chip_id in globals()[f'passed_chip_{i}_{l}']:
                if passed_chip_id in globals()[f'failed_chip_{i}_{l}']:
                    globals()[f'failed_chip_{i}_{l}'].remove(passed_chip_id)
    # for this next bit, it will be good to track how many failures of each test mode occurred
    for i in batch_numbers:
        globals()[f'failed_test_count_{i}_{l}'] = numpy.zeros(8)
    # (2) this next round tackles the pass condition where a chip might fail one test type each round, but so long as it passes each test type at least once, it counts as a passed chip; this only needs to be done for the chips in the failed_chips
    for i in batch_numbers:
        if f'data_table_reduced_{i}_{l}' in globals():
            globals()[f'failed_chip_dummy_{i}_{l}'] = globals()[f'failed_chip_{i}_{l}']
            for failed_chip_id in globals()[f'failed_chip_dummy_{i}_{l}']:
                # we first need to tag the runs where a failed chip was tested multiple times
                repeat_failed_index = []
                for index, test_data in enumerate(globals()[f'data_table_reduced_{i}_{l}']):
                    if failed_chip_id == test_data[1]:
                        repeat_failed_index.append(index)
                # we now tabulate all the failed runs
                failed_chip_runs = []
                for j in repeat_failed_index:
                    failed_chip_runs.append(globals()[f'data_table_reduced_{i}_{l}'][j])
                # before going further, it will be useful to know how many failed runs occurred
                number_of_failed_runs = len(repeat_failed_index)
                # now, to check each test for every run, it will be useful to transpose the table failed_chip_runs
                failed_chip_runs_transpose = list(zip(*failed_chip_runs))
                # from here, we'll just count the number of 'Failed' each test type got. If it's any less than the total number of test runs, that chip passed that test type at some point; if such holds for all tests, then it passed
                indicator = 0
                for j in range(5, 13):
                    if failed_chip_runs_transpose[j].count('Failed') == number_of_failed_runs:
                        if f'failed_data_table_{i}_{l}' in globals():
                            globals()[f'failed_data_table_{i}_{l}'].extend(failed_chip_runs)
                        else:
                            globals()[f'failed_data_table_{i}_{l}'] = failed_chip_runs
                        globals()[f'failed_test_count_{i}_{l}'][j - 5] += 1
                    else:
                        indicator += 1
                        if indicator == 8:
                            globals()[f'passed_chip_{i}_{l}'].append(failed_chip_id)
                            globals()[f'failed_chip_{i}_{l}'].remove(failed_chip_id)
            # we now write out all the failed test tables to .csv files
            if os.path.exists(os.path.join(output_directory, f'failed_data_table_{i}_{l}.csv')):
                with open(os.path.join(output_directory, f'failed_data_table_{i}_{l}.csv'), 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerows(globals()[f'failed_data_table_{i}_{l}'])
            else:
                with open(os.path.join(output_directory, f'failed_data_table_{i}_{l}.csv'), 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerows(globals()[f'failed_data_table_{i}_{l}'])


for l in test_env:
    # now comes the actual numerics
    for i in batch_numbers:
        if f'data_table_reduced_{i}_{l}' in globals():
            globals()[f'passed_chip_number_{i}_{l}'] = len(list(set(globals()[f'passed_chip_{i}_{l}'])))
            globals()[f'failed_chip_number_{i}_{l}'] = len(list(set(list(zip(*globals()[f'failed_data_table_{i}_{l}']))[1])))
    for i in batch_numbers:
        globals()[f'total_tested_chips_{l}'] = 0
        globals()[f'total_passed_chips_{l}'] = 0
        globals()[f'total_failed_chips_{l}'] = 0
    for i in batch_numbers:
        if f'data_table_reduced_{i}_{l}' in globals():
            globals()[f'total_tested_chips_{l}'] = globals()[f'total_tested_chips_{l}'] + globals()[f'passed_chip_number_{i}_{l}'] + globals()[f'failed_chip_number_{i}_{l}']
            globals()[f'total_passed_chips_{l}'] = globals()[f'total_passed_chips_{l}'] + globals()[f'passed_chip_number_{i}_{l}']
            globals()[f'total_failed_chips_{l}'] = globals()[f'total_failed_chips_{l}'] + globals()[f'failed_chip_number_{i}_{l}']
    try:
        globals()[f'total_yield_{l}'] = globals()[f'total_passed_chips_{l}']/globals()[f'total_tested_chips_{l}']
    except ZeroDivisionError:
        globals()[f'total_yield_{l}'] = 'No Tests'
    for i in batch_numbers:
        if f'data_table_reduced_{i}_{l}' in globals():
            globals()[f'chips_{i}_tested_{l}'] = globals()[f'passed_chip_number_{i}_{l}'] + globals()[f'failed_chip_number_{i}_{l}']
            globals()[f'yield_{i}_{l}'] = globals()[f'passed_chip_number_{i}_{l}']/globals()[f'chips_{i}_tested_{l}']

fate_data_labels = []
fate_data = []

for l in test_env:
    fate_data_labels.append(f'{l} # of Chips Tested')
    fate_data_labels.append(f'{l} # of Chips Passed')
    fate_data_labels.append(f'{l} # of Chips Failed')
    fate_data_labels.append(f'{l} Yield')
    for i in batch_numbers:
        if f'data_table_reduced_{i}_{l}' in globals():
            fate_data_labels.append(f'{l} Batch {i} # of Chips Tested')
            fate_data_labels.append(f'{l} Batch {i} # of Chips Passed')
            fate_data_labels.append(f'{l} Batch {i} # of Chips Failed')
            fate_data_labels.append(f'{l} Batch {i} Yield')
    fate_data.append(globals()[f'total_tested_chips_{l}'])
    fate_data.append(globals()[f'total_passed_chips_{l}'])
    fate_data.append(globals()[f'total_failed_chips_{l}'])
    fate_data.append(globals()[f'total_yield_{l}'])
    for i in batch_numbers:
        if f'data_table_reduced_{i}_{l}' in globals():
            fate_data.append(globals()[f'chips_{i}_tested_{l}'])
            fate_data.append(globals()[f'passed_chip_number_{i}_{l}'])
            fate_data.append(globals()[f'failed_chip_number_{i}_{l}'])
            fate_data.append(globals()[f'yield_{i}_{l}'])

with open(os.path.join(output_directory, 'yield_data.csv'), 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(list(zip(*[fate_data_labels, fate_data])))

# this bunch of code writes out the new directories into testSupDirs.csv so they aren't scanned again
if os.path.exists(os.path.join(output_directory, 'testSupDirs.csv')):
    with open(os.path.join(output_directory, 'testSupDirs.csv'), 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for i in test_sup_dir_paths_new:
            writer.writerow([i])
else:
    with open(os.path.join(output_directory, 'testSupDirs.csv'), 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for i in test_sup_dir_paths_new:
            writer.writerow([i])
