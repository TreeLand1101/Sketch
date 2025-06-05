#!/bin/sh

make

datasets="../../equinix-chicago.dirA.20160121-140000.UTC.anon.dat"

memory="200000"
alpha="0.0001"

# for dataset in $datasets; do
#     ./MomentumCDF ${memory} ${alpha} ${dataset}
#     echo "Finished run: memory=${memory}, alpha=${alpha}, dataset=${dataset}"
# done

python3 PlotCDF.py $datasets
