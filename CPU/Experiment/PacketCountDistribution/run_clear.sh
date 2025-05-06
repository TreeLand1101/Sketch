#!/bin/sh

datasets="../../202111011400.dat ../../202211011400.dat ../../equinix-chicago.dirA.20160121-140000.UTC.anon.dat ../../equinix-nyc.dirA.20180315-125910.UTC.anon.dat ../../equinix-nyc.dirA.20190117-125910.UTC.anon.dat"

echo ">>> Clearing PNG files in dataset directories..."

stems=""
for f in $datasets; do
  if [ ! -f "$f" ]; then
    echo "Warning: file not found: $f"
    continue
  fi
  stem=$(basename "$f" .dat)
  stems="$stems $stem"
done

for stem in $stems; do
  if [ -d "$stem" ]; then
    find "$stem" -type f -name "*.png" -delete
    echo "Cleared PNGs in $stem"
  else
    echo "Warning: directory not found: $stem"
  fi
done

echo ">>> PNG cleanup complete."