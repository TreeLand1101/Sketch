#include "BenchMark.h"
#include <fstream>
#include <vector>
#include <string>
#include <iostream>
#include <iomanip>
#include <utility>

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <memory> <alpha> <dataset1> [dataset2] ..." << std::endl;
        return 1;
    }
    
    uint32_t memory = std::stoi(argv[1]);
    double alpha = std::stod(argv[2]);
    
    std::vector<double> forward_ratios = {
        0.5, 
        0.55, 
        0.6, 
        0.65, 
        0.7, 
        0.75, 
        0.8, 
        0.85, 
        0.9
    };

    std::vector<std::pair<double, double>> memory_ratios = {
        {0.5, 0.5},
        {0.6, 0.4},
        {0.7, 0.3},
        {0.8, 0.2},
        {0.9, 0.1}
    };
    
    std::ofstream ofs("heatmap_results.csv");
    ofs << "Dataset,FilterRatio,SketchRatio,ForwardRatio,F1score,Precision,Recall,InsertTime,QueryTime" << std::endl;
    
    for (uint32_t i = 3; i < static_cast<uint32_t>(argc); ++i) {
        std::cout << argv[i] << std::endl;
        BenchMark dataset(argv[i], "Dataset");
        for (auto& ratio_pair : memory_ratios) {
            double filter_ratio = ratio_pair.first;
            double sketch_ratio = ratio_pair.second;
            for (double forward_ratio : forward_ratios) {
                Metrics metrics = dataset.HHBenchWithMetrics(memory, alpha, filter_ratio, sketch_ratio, forward_ratio);
                ofs << argv[i] << ","
                    << filter_ratio << ","
                    << sketch_ratio << ","
                    << forward_ratio << ","
                    << metrics.f1score << ","
                    << metrics.precision << ","
                    << metrics.recall << ","
                    << metrics.avgInsertTime << ","
                    << metrics.avgQueryTime << std::endl;
            }
        }
    }
    
    ofs.close();
    std::cout << "CSV output saved to heatmap_results.csv" << std::endl;
    return 0;
}
