#!/bin/bash

run_benchmark() {
    local concurrency_levels=(5 10 15 20 30 40 50 60 70 80 90 100)
    local payload_file=$1
    local url=$2
    local num_runs=$3
    local endpoint=$4
    echo "endpoint is$payload_file"

    for concurrency in "${concurrency_levels[@]}"; do
        local result_file="data_${endpoint}_concurrency_${concurrency}.csv"
        for ((run=1; run<=num_runs; run++)); do
            echo "=== Run $run for concurrency $concurrency ==="
            ab -n $concurrency -c $concurrency -e $result_file -p $payload_file -T "application/json" "$url/$endpoint"
            echo "===================="
        done
    done
}

# Example usage:

payload_file="payload.json"
num_runs=5
url="http://10.52.0.201:7000"

run_benchmark  $payload_file $url $num_runs cpu
run_benchmark  $payload_file $url $num_runs infer
