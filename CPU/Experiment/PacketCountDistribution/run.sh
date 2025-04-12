#!/bin/sh

make

./PacketCountDistribution

python3 PlotPacketCountDistribution.py