#!/bin/sh

memory=500000

threshold=0.0001

log_path=Result/memory_${memory}_threshold_${threshold}.txt

datset=equinix-chicago.dirA.20160121-140000.UTC.anon.dat

mkdir -p $(dirname ${log_path})

make

./CPU ${memory} ${threshold} ${datset} >> ${log_path}