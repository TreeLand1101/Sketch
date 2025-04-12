#include "MMap.h"
#include "TwoStage.h"

#include <unordered_map>
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>

struct Metrics {
    double f1score;
    double precision;
    double recall;
    double aae;
    double are;
    double avgInsertTime;
    double avgQueryTime;
};

class BenchMark {
public:
    BenchMark(const std::string &PATH, const std::string &name) {
        fileName = name;
        result = Load(PATH.c_str());
        dataset = (TUPLES*)result.start;
        length = result.length / sizeof(TUPLES);
        for (uint64_t i = 0; i < length; ++i) {
            tuplesMp[dataset[i]] += 1;
        }
    }

    ~BenchMark() {
        UnLoad(result);
    }

    Metrics HHBenchWithMetrics(uint32_t MEMORY, double alpha, double FILTER_RATIO, double SKETCH_RATIO, double ADMISSION_RATIO) {
        COUNT_TYPE threshold = alpha * length;
        TwoStage<TUPLES>* tupleSketch = new TwoStage<TUPLES>(MEMORY, threshold, FILTER_RATIO, SKETCH_RATIO, ADMISSION_RATIO);

        Metrics metrics = ComputeMetrics(tupleSketch, threshold, alpha);

        delete tupleSketch;
        return metrics;
    }

private:
    std::string fileName;
    LoadResult result;
    TUPLES* dataset;
    uint64_t length;
    std::unordered_map<TUPLES, COUNT_TYPE> tuplesMp;

    Metrics ComputeMetrics(TwoStage<TUPLES>* tupleSketch, COUNT_TYPE threshold, double alpha) {
        TP start, end;
        double avgInsertTime = 0, avgQueryTime = 0;

        start = std::chrono::high_resolution_clock::now();
        for (uint32_t j = 0; j < length; ++j) {
            tupleSketch->Insert(dataset[j]);
        }
        end = std::chrono::high_resolution_clock::now(); 

        avgInsertTime = durationms(end, start) / length;

        start = std::chrono::high_resolution_clock::now();
        for (uint32_t j = 0; j < length; ++j) {
            tupleSketch->Query(dataset[j]);
        }
        end = std::chrono::high_resolution_clock::now();

        avgQueryTime = durationms(end, start) / length;

        std::unordered_map<TUPLES, COUNT_TYPE> estTuple = tupleSketch->AllQuery();

        double realHH = 0, estHH = 0, bothHH = 0, aae = 0, are = 0;
        for (auto it = tuplesMp.begin(); it != tuplesMp.end(); ++it) {
            bool real = (it->second > threshold);
            double estF = estTuple[it->first];
            bool est = (estF > threshold);
            realHH += real;
            estHH += est;
            if (real && est) {
                bothHH += 1;
                aae += std::abs(it->second - estF);
                are += std::abs(it->second - estF) / it->second;
            }
        }
        double recall = (realHH > 0) ? bothHH / realHH : 0;
        double precision = (estHH > 0) ? bothHH / estHH : 0;
        double f1score = (precision + recall > 0) ? 2 * (precision * recall) / (precision + recall) : 0;

        Metrics metrics;
        metrics.f1score = f1score;
        metrics.precision = precision;
        metrics.recall = recall;
        metrics.aae = (bothHH > 0) ? aae / bothHH : 0;
        metrics.are = (bothHH > 0) ? are / bothHH : 0;
        metrics.avgInsertTime = avgInsertTime;
        metrics.avgQueryTime = avgQueryTime;
        return metrics;
    }
};

