#!/bin/sh

# Compile the program
make

# Dataset file
datasets="equinix-nyc.dirA.20180315-125910.UTC.anon.dat"

# Configurable parameters
memory_values="50000 75000 100000 125000 150000"
alphas="0.0001"

# Nested loops for memory and threshold combinations
for dataset in $datasets 
do
    # Create the Performance/{dataset} directory if it doesn't exist
    mkdir -p "Performance/${dataset}"
    
    for memory in $memory_values
    do
        for alpha in $alphas
        do
            log_path="Performance/${dataset}/memory_${memory}_alpha_${alpha}.txt"
            ./CPU ${memory} ${alpha} ${dataset} >> ${log_path}
            echo "Finished run: memory=${memory}, alpha=${alpha} for dataset=${dataset}"
        done
    done
    python3 metric.py "$dataset" "$alphas" $memory_values
done

echo "Finished all runs and generated plots."