#include "BenchMark.h"
#include <cstdio>
#include <vector>
#include <string>
#include <iostream>
#include <iomanip>
#include <utility>
#include <cstdlib>

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <memory> <alpha> <dataset1> [dataset2] ..." << std::endl;
        return 1;
    }
    
    uint32_t memory = std::stoi(argv[1]);
    double alpha = std::stod(argv[2]);
    
    std::vector<double> admission_ratios = {
        0.3,
        0.4,
        0.5, 
        0.6, 
        0.7, 
        0.8, 
        0.9
    };

    std::vector<std::pair<double, double>> memory_ratios = {
        {0.3, 0.7},
        {0.4, 0.6},
        {0.5, 0.5},
        {0.6, 0.4},
        {0.7, 0.3},
    };
    
    FILE* fp = fopen("heatmap_results.csv", "w");
    if (fp == nullptr) {
        std::cerr << "Cannot open file heatmap_results.csv" << std::endl;
        return 1;
    }
    
    fprintf(fp, "Dataset,FilterRatio,SketchRatio,AdmissionRatio,F1score,Precision,Recall,InsertTime,QueryTime\n");
    
    for (uint32_t i = 3; i < argc; ++i) {
        std::cout << argv[i] << std::endl;
        BenchMark dataset(argv[i], "Dataset");
        for (auto& ratio_pair : memory_ratios) {
            double filter_ratio = ratio_pair.first;
            double sketch_ratio = ratio_pair.second;
            for (double admission_ratio : admission_ratios) {
                Metrics metrics = dataset.HHBenchWithMetrics(memory, alpha, filter_ratio, sketch_ratio, admission_ratio);
                          
                fprintf(fp, "%s,%.2f,%.2f,%.2f,%.6f,%.6f,%.6f,%.6f,%.6f\n", 
                        argv[i], 
                        filter_ratio, 
                        sketch_ratio, 
                        admission_ratio, 
                        metrics.f1score, 
                        metrics.precision, 
                        metrics.recall, 
                        metrics.avgInsertTime, 
                        metrics.avgQueryTime);
            }
        }
    }
    
    fclose(fp);
    std::cout << "CSV output saved to heatmap_results.csv" << std::endl;
    return 0;
}
