#!/bin/sh

# Compile the program
make

# Dataset file
dataset="equinix-chicago.dirA.20160121-140000.UTC.anon.dat"

# Configurable parameters
memory_values="50000 100000 150000 200000 250000"
threshold_values="0.0001" 

# Nested loops for memory and threshold combinations
for memory in $memory_values
do
    for threshold in $threshold_values
    do
        log_path="Result/memory_${memory}_threshold_${threshold}.txt"
        mkdir -p $(dirname ${log_path})
        ./CPU ${memory} ${threshold} ${dataset} >> ${log_path}
        echo "Finished run: memory=${memory}, threshold=${threshold}"
    done
done

echo "Finished all run."