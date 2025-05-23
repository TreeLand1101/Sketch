#!/bin/sh

# Compile the program
make

# Dataset file
dataset="../../equinix-chicago.dirA.20160121-140000.UTC.anon.dat"

# Configurable parameters
memory_values="100000"
threshold_values="0.0001" 

# Nested loops for memory and threshold combinations
for memory in $memory_values
do
    for threshold in $threshold_values
    do
        ./ParameterHeatmap ${memory} ${threshold} ${dataset}
        echo "Finished run: memory=${memory}, threshold=${threshold}"
    done
done

echo "Finished all run."

python3 PlotHeatmap.py