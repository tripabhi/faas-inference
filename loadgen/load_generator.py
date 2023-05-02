#!/usr/bin/env python3
import httpx
import json
import time
import sys
import os
import csv
import concurrent.futures
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-gip", "--gateway_ip", type=str, default="127.0.0.1", help="Mention the gateway ip")
parser.add_argument("-p", "--port", type=str, default="5000", help="Mention the gateway port")
parser.add_argument("-n", "--num_requests", type=int, default=10, help="Number of requests to send")
parser.add_argument("-f", "--function_name", type=str, help="Name of the function to invoke")
parser.add_argument("-m", "--message", type=str, help="add message", default="Just had the best meal at this new restaurant! The food was amazing - fresh, flavorful, and beautifully presented. The service was top-notch too, with friendly and attentive staff who made sure we had everything we needed. Can't wait to come back for more!")
parser.add_argument("-pmm", "--print_model_metrics", action='store_true', help="Print model metrics")
args = parser.parse_args()

FUNCTION_NAME = args.function_name
GATEWAY_IP = args.gateway_ip
PORT = args.port
MESSAGE = args.message

url = 'http://{}:{}/serve'.format(GATEWAY_IP, PORT)
headers = {'Content-Type': 'application/json'}
data = {'data': MESSAGE}



print(url)

def convert_to_ms(num):
    return int(round(num*1000))

def send_request(url, headers, data):
    start_time = time.monotonic()
    lent = 0
    # print send request timestamp
    print("Sending request timestamp: {}".format(datetime.datetime.now().time()))
    while lent < 1:
        r = httpx.post(url, headers=headers, data=data)
        lent = len(r.text)
    end_time = time.monotonic()
    response_time = convert_to_ms(end_time - start_time)
    return response_time, r.text

num_requests = args.num_requests
response_futures = []

with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
    for i in range(num_requests):
        future = executor.submit(send_request, url, headers, json.dumps(data))
        response_futures.append(future)

avg_response_time = 0
min_response_time = float('inf')
tail_response_times = []

responses = [future.result() for future in concurrent.futures.as_completed(response_futures)]

for response_time, response_text in responses:
    avg_response_time += response_time
    if response_time < min_response_time:
        min_response_time = response_time
    tail_response_times.append(response_time)

avg_response_time /= num_requests
tail_response_times = sorted(tail_response_times)[int(num_requests * 0.99):]
headers = ['BurstRequests', 'FunctionName', 'MessageLength','ModelLoadTime', 'TokenTime', 'InferenceTime', 'TotalTime', 'ResponseTime', 'data']
for i, (response_time, response_text) in enumerate(responses):
    data = json.loads(response_text)
    labels_string = data['labels']
    labels = json.loads(labels_string)
    labels["FunctionName"] = FUNCTION_NAME
    labels["ResponseTime"] = response_time
    labels["MessageLength"] = len(MESSAGE)
    labels['BurstRequests'] = num_requests
    if args.print_model_metrics:
        print("FunctionName: {}".format(labels['FunctionName']))
        print("ModelLoadTime: {} ms".format(labels['ModelLoadTime']))
        print("TokenTime: {} ms".format(labels['TokenTime']))
        print("InferenceTime: {} ms".format(labels['InferenceTime']))
        print("TotalTime: {} ms".format(labels['TotalTime']))
        print("ResponseTime: {} ms".format(labels['ResponseTime']))
        print("*********")
    with open('results/model_metrics.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerow(labels)

print("Average response time: {} ms".format(avg_response_time))
print("Minimum response time: {} ms".format(min_response_time))
print("Tail response times: {} ms".format(tail_response_times))
