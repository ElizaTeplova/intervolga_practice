import requests as r
import json
import pandas as pd
import regex as re
import csv
from requests import HTTPError
import time
import os
from RequestParams import RequestParams


# STEP 0 is checking possibility of request execution according demand parameters
def evaluate_request(counter_id: str, token: str, request_params: RequestParams) -> bool:
    url = f'https://api-metrika.yandex.net/management/v1/counter/{counter_id}/logrequests/evaluate'
    headers = {'Authorization': f'Bearer {token}'}
    fields = {
        'date1': request_params.start_date,
        'date2': request_params.end_date,
        'fields': ','.join(request_params.fields),
        'source': request_params.source
    }
    response = r.get(url, headers=headers, params=fields)

    if response.status_code != 200:
        print(response.text)
        raise HTTPError(response.status_code)
    possible = response.json()['log_request_evaluation']['possible']
    if not possible:
        print(f'Request with params {request_params} could not be executed')
    return possible


# STEP 1 is creating log file according to your willingness. Additioal request is provided as
# https://api-metrika.yandex.net/management/v1/counter/{counter_id}/logrequests/evaluate but anyway you would be
# notified if smth went wrong

# The output is request_id (int/string) according to parameters, which were provided
def create_logs(counter_id: str, token: str, request_params: RequestParams) -> str:
    url = 'https://api-metrika.yandex.net/management/v1/counter/5227786/logrequests'
    headers = {'Authorization': f'Bearer {token}'}
    fields = {
        'date1': request_params.start_date,
        'date2': request_params.end_date,
        'fields': ','.join(request_params.fields),
        'source': request_params.source
    }
    response = r.post(url, headers=headers, params=fields)

    if response.status_code != 200:
        raise HTTPError(response.status_code)

    request_id = response.json()['log_request']['request_id']

    return request_id


# STEP 2 is getting amount of parts which your log was separated.
# It could vary from 7 to 120 seconds

# The output is amount of parts which data was separated.
def get_parts_number(counter_id: str, token: str, request_id: str) -> int:
    url = f"https://api-metrika.yandex.net/management/v1/counter/{counter_id}/logrequest/{request_id}"
    headers = {'Authorization': f'Bearer {token}'}

    while True:
        response = r.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPError(response.status_code)
        if response.json()['log_request']['status'] == 'processed':
            break
        print(f"Request id: {request_id} Status: {response.json()['log_request']['status']}")
        time.sleep(5)

    print(f"Request id: {request_id} Status: {response.json()['log_request']['status']}")
    part_numbers = len(response.json()['log_request']['parts'])
    return part_numbers


def save_to_csv_file(tsv_data, counter_id: str, request_id: str, part: int) -> str:
    rows = tsv_data.split("\n")
    filename = f"output{counter_id}_{request_id}_{part}.csv"
    csv_writer = csv.writer(open(filename, "w", newline="", encoding="utf-8"))
    for row in rows:
        columns = row.split("\t")
        csv_writer.writerow(columns)
    print(f"File {filename} created")
    return filename


# STEP 3 is getting all this parts.

# Provided data has TSV format, thus we convert and save this data in csv files and altogether.
def download_data(counter_id: str, token: str, request_id: str, parts: int, clean_partial_files: bool = True) -> None:
    headers = {'Authorization': f'Bearer {token}'}
    filenames = []
    for part_number in range(parts):
        url = f"https://api-metrika.yandex.net/management/v1/counter/{counter_id}/logrequest/{request_id}/part/{part_number}/download"
        response = r.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPError(response.status_code)
        filename = save_to_csv_file(response.text, counter_id, request_id, part_number)
        filenames.append(filename)

    dfs = []
    for filename in filenames:
        dfs.append(pd.read_csv(filename))
    merged_df = pd.concat(dfs, ignore_index=True)

    filename_all = f'output{counter_id}_{request_id}_all.csv'
    merged_df.to_csv(filename_all, index=False)
    print(f"File {filename_all} saved")

    if clean_partial_files:
        for filename in filenames:
            os.remove(filename)
            print(f"File {filename} was removed")


# STEP 4 is cleaning log file if necessary
def clean_logfile(counter_id: str, token: str, request_id: str) -> None:
    url = f"https://api-metrika.yandex.net/management/v1/counter/{counter_id}/logrequest/{request_id}/clean"
    headers = {'Authorization': f'Bearer {token}'}
    response = r.post(url, headers=headers)
    if response.status_code != 200:
        raise HTTPError(response.status_code)
    print(f"Log request: {request_id} was successfully removed")

    # COUNTER_ID and TOKEN must be written manually for security purposes


def main(counter_id: str, token: str, request_params: RequestParams, clean_log=False, clean_partial_files=True) -> None:
    possible = evaluate_request(counter_id, token, request_params)
    if not possible:
        return
    request_id = create_logs(counter_id, token, request_params)
    part_numbers = get_parts_number(counter_id, token, request_id)
    download_data(counter_id, token, request_id, part_numbers, clean_partial_files)
    if clean_log:
        clean_logfile(counter_id, token, request_id)


if __name__ == "__main__":
    COUNTER_ID = str(input("Input counter ID: "))
    TOKEN = str(input("Input token: "))
    REQUEST_PARAMS = RequestParams()

    main(counter_id=COUNTER_ID,
         token=TOKEN,
         request_params=REQUEST_PARAMS,
         clean_log=True,
         clean_partial_files=True)
