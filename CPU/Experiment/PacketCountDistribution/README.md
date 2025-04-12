Requirements
-------
- cmake
- g++
- matplotlib
- numpy

How to run
```bash
$ cmake .
$ sh run.sh
```

Dump first 50000 from pcap
```bash
$ tcpdump -r equinix-chicago.dirA.20160121-140000.UTC.anon.pcap -w equinix-chicago.dirA.20160121-140000.UTC.anon_first_50000.pcap -c 50000
```