#-*- coding: UTF-8  -*-
"""
#@author:GloriaKatunge

"""

import csv
import multiprocessing
import os
import re
import time
from datetime import datetime

# Set your DRIVE_PATH and TARGET_FILE here
DRIVE_PATH = "C:\LArASIC_QC"
TARGET_FILE = 'Result.csv'
AVAILABLE_TESTS = [
    "Power Measurement", "FE parameter measurement", "Channel Response (Internal DAC) @SDD_OFF",
    "Channel Response (Internal DAC) @SDD_ON", "Channel Response (Ext Pulse) @", "BL Restore Test",
    "FE Power Cycle", "FE gain plot (DAC pulsing)"
]

def process_digits(value):
    batch_number_processed = ''
    chip_id_unprocessed = ''

    # this if statement is needed to ensure the batch and chip id string is actually a number
    if value.isdigit():
        # this if statement handles the case if there are less than 5 numbers in the index, nly happens for batch 000
        if len(value) < 5:
            batch_number_processed = '000'
            chip_id_unprocessed = value
        # this if statement handles the possibility that there are 5 digits in the raw batch/chip ID; If the value
        # is < 10,000, it is batch 000; if it is > 9,999, the first digit is the batch # and the last 4 are the chip ID
        elif len(value) == 5:
            if int(value) <= 9999:
                batch_number_processed = '000'
                chip_id_unprocessed = value
            else:
                batch_number_processed = f'00{value[0]}0'
                chip_id_unprocessed = value[1:]
        # this else if statement handles the case when there are three 0's at the start of the index, which should
        # only ever occur for batch 000
        elif '000' in value[:3]:
            batch_number_processed = '000'
            chip_id_unprocessed = value.lstrip(batch_number_processed)
        else:
            for char_index, char in enumerate(value):
                y = int(char)
                if y > 0:
                    batch_number_processed = f'00{value[char_index]}{value[char_index + 1]}'
                    # for this case, when stripping away the batch_number_unprocessed from the raw string to get the
                    # chip_id_unprocessed, it is imperative to also strip the next character as well, as that is the
                    # second 1, which is also part of the batch number
                    chip_id_unprocessed = value.lstrip(value[:char_index + 1])
                    # this if statement tackles the batch 0011 (1.1), since there should be no opportunity for a 1 to
                    # appear right after the first 1 unless the chip is in batch 0011; this is the general principle
                    # that should be used for sub-batches (e.g. batch 2.5)
                    break
    else:
        return None
    # the rest of the function is dedicated to normalizing the chip ID's into 5-digit values
    chip_id_deficiency_length = 5 - len(chip_id_unprocessed)
    chip_id_processed = '0' * chip_id_deficiency_length + chip_id_unprocessed

    batch_no_deficiency_length = 4 - len(batch_number_processed)
    batch_no_processed = '0' * batch_no_deficiency_length + batch_number_processed

    return f'{batch_no_processed}-{chip_id_processed}'


def get_folder_name(abs_path):
    return os.path.basename(os.path.dirname(abs_path))


def get_environment_from_path(absolut_path):
    folder_name = get_folder_name(absolut_path)
    match = re.search(r'_(RT|LN)(?:$|[^A-Za-z0-9])', folder_name)
    return match.group(1) if match else None


def clean_files(files):
    incomplete = []
    complete = []
    for result in files:
        file_with_batch_no_chip_id_arr = result.split(' | ')
        if file_with_batch_no_chip_id_arr[1] == '':
            incomplete.append(file_with_batch_no_chip_id_arr[0])
        else:
            complete.append(f'{file_with_batch_no_chip_id_arr[0]} | {file_with_batch_no_chip_id_arr[1]}')

    return complete, incomplete


def get_batch_no_chip_id(path):
    batch_no_chip_id = ''
    pattern = r'[^_]*_(\d+)_'

    folder_name = os.path.basename(os.path.dirname(path))
    match = re.search(pattern, folder_name)

    if match:
        batch_no_chip_id = process_digits(match.group(1).zfill(5))

    return batch_no_chip_id


def search_csv_files_in_directory(directory):
    csv_files = []
    for root, _, files in os.walk(directory):
        if not any(directory.startswith('.') for directory in os.path.basename(root).split(os.path.sep)):
            for file in files:
                if file.lower() == TARGET_FILE.lower():
                    csv_files.append(os.path.join(root, file))
    return csv_files


def process_csv_file_paths(directory):
    csv_files = search_csv_files_in_directory(directory)
    result_csv_dict = []
    for file in csv_files:
        batch_no_chip_id = get_batch_no_chip_id(file)
        if batch_no_chip_id is not None:
            result_csv_dict.append(f'{file} | {batch_no_chip_id}')
    return result_csv_dict


def process_incomplete_files(files, start):
    current_timestamp = datetime.now()
    timestamp = current_timestamp.strftime('%Y_%m_%d_%H_%M_%S')
    for file in files:
        path_name = os.path.join('Results', f'{timestamp}_incomplete.csv')
        result_dir = os.path.join(DRIVE_PATH, path_name)

        data = [file]

        # Creating directory if it doesn't exist
        directory = os.path.dirname(result_dir)
        if directory:
            os.makedirs(directory, exist_ok=True)

        mode = 'a' if os.path.exists(result_dir) else 'w'

        with open(result_dir, mode, newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if mode == 'w':
                csvwriter.writerow(['FILE_PATH'])  # Writing header
            csvwriter.writerow(data)  # Writing data

    end = time.time()  # Record the end time
    total_execution_time = round((end - start), 6)
    print(f"\nTook: {total_execution_time}s to write {len(files)} result for incomplete files\n")


def process_complete_files(files, start):
    abs_path_with_tests = {}
    for file_res in files:
        if 'RT' in file_res:
            file_res_arr = file_res.split(' | ')
            abs_path = file_res_arr[0]
            batch_no_chip_id = file_res_arr[1]

            results = {}
            with open(abs_path, 'r') as csv_file:
                for row in csv.reader(csv_file):
                    if len(row) == 2:
                        row_with_test_name = row[0].strip()
                        row_with_result_name = row[1].strip()

                        if row_with_test_name in results:
                            results[f'{row_with_test_name} {row_with_result_name}'] = row_with_result_name
                        else:
                            results[row_with_test_name] = row_with_result_name
                        abs_path_with_tests[f'{abs_path} | {batch_no_chip_id}'] = results

    end = time.time()  # Record the end time
    total_execution_time = round((end - start), 6)
    print(f"Took: {total_execution_time}s to read through {len(abs_path_with_tests)} Result.csv files")

    return abs_path_with_tests


def write_csv_result_files(decisions, timestamp, start):
    for val in decisions:
        b, ch, dec, abs_path = val.split(',')
        data = [ch.strip(), dec.strip(), abs_path.strip()]

        file_name = f'batch_{b.strip()}_passed.csv' if dec.strip() == 'Passed' else f'batch_{b.strip()}_failed.csv'
        path_name = os.path.join('Results', f'{timestamp}_{file_name}')
        result_dir = os.path.join(DRIVE_PATH, path_name)

        # Creating directory if it doesn't exist
        directory = os.path.dirname(result_dir)
        if directory:
            os.makedirs(directory, exist_ok=True)

        mode = 'a' if os.path.exists(result_dir) else 'w'

        with open(result_dir, mode, newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if mode == 'w':
                csvwriter.writerow(['CHIP_ID', 'STATUS', 'FILE_PATH'])  # Writing header
            csvwriter.writerow(data)  # Writing data

    end = time.time()  # Record the end time
    total_execution_time = round((end - start), 6)
    print(f"Took: {total_execution_time}s to write {len(decisions)} result files")


def count_passed_failed_results_per_batch(aggregate, start):
    if len(aggregate) > 0:
        # Initialize dictionaries to count passed and failed results for each batch_no
        passed_counts = {}
        failed_counts = {}

        # Collect all unique batch_no values from aggregated_results
        unique_batch_nos = set(batch_no_chip_id.split('-')[0] for batch_no_chip_id in aggregate.keys())

        # Initialize counts for all unique batch_no values
        for batch_no in unique_batch_nos:
            passed_counts[batch_no] = 0
            failed_counts[batch_no] = 0

        # Iterate through aggregated_results
        for batch_no_chip_id, result_dict in aggregate.items():
            batch_no, _, _ = batch_no_chip_id.split('-')  # Split batch_no_chip_id to get batch_no

            # Get the final decision for this result_dict
            final_decision = "Passed" if all(result == "Passed" for result in result_dict["results"]) else "Failed"

            # Update the counts based on the final decision
            if final_decision == "Passed":
                passed_counts[batch_no] += 1
            else:
                failed_counts[batch_no] += 1

        print(f'\n========== (Summary for {len(aggregate)} files) =============')
        # Now, passed_counts and failed_counts contain the counts of passed and failed results for each batch_no
        for batch_no, passed_count in passed_counts.items():
            failed_count = failed_counts.get(batch_no, 0)
            print(f"Batch No. {batch_no}: Passed: {passed_count}, Failed: {failed_count}")

        end = time.time()  # Record the end time
        total_execution_time = round((end - start), 7)
        print(f'========== (Took {round((total_execution_time / 60), 6)}m to execute) ==========')


def determine_chip_decision(results, start):
    # Dictionary to store the aggregated results for each batch_no_chip_id
    aggregated_results = {}
    decision_list = []

    current_timestamp = datetime.now()
    formatted_timestamp = current_timestamp.strftime('%Y_%m_%d_%H_%M_%S')

    for file_path, inner_dict in results.items():
        # Extract batch_no_chip_id from file_path

        path, batch_no_chip_id = file_path.split('|')
        environment = get_environment_from_path(path)

        # Initialize or retrieve the result dictionary for the current batch_no_chip_id
        result_dict = aggregated_results.get(
            f'{batch_no_chip_id.strip()}-{environment}', {"path": path.strip(), "results": []}
        )

        for test, value in inner_dict.items():
            if test not in AVAILABLE_TESTS:
                stripped = test.rstrip(" Passed").rstrip(" Failed") if 'Passed' in test or 'Failed' in test else test
                if stripped in AVAILABLE_TESTS:
                    final_val = 'Passed' if 'Passed' in inner_dict.get(stripped) or 'Passed' in value else 'Failed'
                    inner_dict[stripped] = final_val

        tests_passed = sum(1 for test in AVAILABLE_TESTS if inner_dict.get(test, "") == "Passed") > 6

        # tests_passed = all(inner_dict.get(test, "") == "Passed" for test in AVAILABLE_TESTS)

        # Append the result for this run to the results list
        result_dict["results"].append("Passed" if tests_passed else "Failed")

        # Update the aggregated_results dictionary with the result dictionary for this batch_no_chip_id
        aggregated_results[f'{batch_no_chip_id}-{environment}'] = result_dict

    # Check and update results if they differ on a second run
    for _, result_dict in aggregated_results.items():
        results = result_dict["results"]
        if len(results) > 1:
            if results[0] != results[1]:
                result_dict["results"][0] = "Passed"

    # Now, aggregated_results contains the updated results with paths
    for batch_no_chip_id_env, result_dict in aggregated_results.items():
        path = result_dict["path"]
        results = result_dict["results"]

        batch_no, chip_id, _ = batch_no_chip_id_env.split('-')
        final_decision = "Passed" if all(result == "Passed" for result in results) else "Failed"
        decision_list.append(f"{batch_no.strip()}, {chip_id}, {final_decision}, {path}")

    end = time.time()  # Record the end time
    total_execution_time = round((end - start), 6)
    print(f"Took: {total_execution_time}s to aggregate {len(aggregated_results)} Result.csv files")

    write_csv_result_files(decision_list, formatted_timestamp, start)
    return aggregated_results


if __name__ == '__main__':
    start_time = time.time()  # Record the start time
    num_processes = multiprocessing.cpu_count()  # Use the number of available CPU cores
    pool = multiprocessing.Pool(processes=num_processes)

    # Divide the DRIVE_PATH into chunks for parallel processing
    chunk_size = len(os.listdir(DRIVE_PATH)) // num_processes
    path_chunks = [os.path.join(DRIVE_PATH, subdir) for subdir in os.listdir(DRIVE_PATH)]

    # Use multiprocessing.Pool to parallelize the processing
    result_lists = pool.map(process_csv_file_paths, path_chunks)

    # Combine the results from all processes into a flat list
    combined_result = [item for sublist in result_lists for item in sublist]

    pool.close()
    pool.join()

    end_time = time.time()  # Record the end time
    execution_time = round((end_time - start_time), 6)

    print(f"Took: {execution_time}s to scan and obtain {len(combined_result)} Result.csv file paths.")

    complete_files, incomplete_files = clean_files(combined_result)

    if len(incomplete_files):
        print(f'\nFound {len(incomplete_files)} without defined batch_no and chip_id\n')
        process_incomplete_files(incomplete_files, start_time)

    if len(complete_files):
        processed_files = process_complete_files(complete_files, start_time)
        aggregate_dict = determine_chip_decision(processed_files, start_time)
        count_passed_failed_results_per_batch(aggregate_dict, start_time)

    entire_end_time = time.time()  # Record the end time
    total_time = round((entire_end_time - start_time), 6)  # to get the value in minutes
    print(f"\nSCRIPT TOOK: {round((total_time / 60), 6)}m TO EXECUTE")
