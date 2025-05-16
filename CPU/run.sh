#!/bin/sh

# Compile the program
make

# Dataset file
dataset="equinix-chicago.dirA.20160121-140000.UTC.anon.dat"

# Configurable parameters
memory_values="25000 50000 75000 100000 125000"
alphas="0.0001" 

# Nested loops for memory and threshold combinations
for memory in $memory_values
do
    for alpha in $alphas
    do
        log_path="Performance/memory_${memory}_alpha_${alpha}.txt"
        ./CPU ${memory} ${alpha} ${dataset} >> ${log_path}
        echo "Finished run: memory=${memory}, alpha=${alpha}"
    done
done

echo "Finished all run."

python3 Performance/metric.py $alphas $memory_values