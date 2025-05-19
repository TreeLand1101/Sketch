#!/bin/sh

RUN_CPP=false
RUN_PY=true

MEMORY=100000
ALPHA=0.0001

datasets="../../202111011400.dat ../../202211011400.dat ../../equinix-chicago.dirA.20160121-140000.UTC.anon.dat ../../equinix-nyc.dirA.20180315-125910.UTC.anon.dat ../../equinix-nyc.dirA.20190117-125910.UTC.anon.dat"

if [ "$RUN_CPP" = true ]; then
  echo ">>> Compiling C++ program..."
  make
fi

stems=""
for f in $datasets; do
  if [ ! -f "$f" ]; then
    echo "Warning: file not found: $f"
    continue
  fi

  if [ "$RUN_CPP" = true ]; then
    echo ">>> Running C++ on: $f"
    ./PacketCountDistribution "$MEMORY" "$ALPHA" "$f"
  fi

  stem=$(basename "$f" .dat)
  stems="$stems $stem"
done

if [ "$RUN_PY" = true ]; then
  echo ">>> Plotting with Python for stems:$stems"
  python3 PlotPacketCountDistribution.py $stems \
      --memory "$MEMORY" --alpha "$ALPHA"
fi

echo ">>> All done."