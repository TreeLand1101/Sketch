Requirements
-------
- cmake
- g++

How to run
```bash
$ cmake .
$ make
$ ./PacketCountDistribution
```

Plot PacketCountDistribution
```python
python3 PlotCDF.py
```

Calculate mice / elephant info
```python
python3 ElephantMiceSums.py
```

Dump first 50000 from pcap
```bash
$ tcpdump -r equinix-chicago.dirA.20160121-140000.UTC.anon.pcap -w equinix-chicago.dirA.20160121-140000.UTC.anon_first_50000.pcap -c 50000
```