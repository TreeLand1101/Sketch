CPU Code
============

Repository structure
--------------------
*  `Common/`: the hash and mmap functions
*  `Struct/`: the data structures, such as heap and hash table
*  `Src/`: sketch algorithms
*  `Benchmark.h`: the benchmarks about ARE, recall rate, and precision rate

Requirements
-------
- cmake
- g++

How to run
-------
- To modify `memory` and the `heavy hitter threshold`, please refer to `run.sh`
- To run on a difference sketch, please refer to `BenchMark.h`

```bash
$ cmake .
$ sh run.sh
```
dat: https://drive.google.com/file/d/1knFXziAxpczhG25EeKdmq1zdfrq1eSb6/view?usp=drive_link
