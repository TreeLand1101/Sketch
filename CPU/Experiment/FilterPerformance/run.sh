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
    ./FilterPerformance ${memory} ${dataset}
    echo "Finished run: memory=${memory}"
done

echo "Finished all run."

python3 metric.py $memory_values