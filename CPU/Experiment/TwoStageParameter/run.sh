#!/bin/sh

make

DATASET_DIR="../../"

dataset="equinix-chicago.dirA.20160121-140000.UTC.anon.dat"

memory_values="128"
threshold_values="0.0001" 

for memory in $memory_values
do
    for threshold in $threshold_values
    do
        ./TwoStageParameter ${memory} ${threshold} "${DATASET_DIR}${dataset}"
        echo "Finished run: memory=${memory}KB, threshold=${threshold}"
    done
done

echo "Finished all run."

python3 PlotHeatmap.py