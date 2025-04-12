#!/bin/sh

# Compile the program
make

# Dataset file
dataset="../../equinix-chicago.dirA.20160121-140000.UTC.anon.dat"

# Configurable parameters
memory_values="25000 50000 75000 100000"

# Nested loops for memory and threshold combinations
for memory in $memory_values
do
    log_path="memory_${memory}_threshold.txt"
    ./FilterPerformance ${memory} ${dataset} >> ${log_path}
    echo "Finished run: memory=${memory}"
done

echo "Finished all run."


python3 metric.py