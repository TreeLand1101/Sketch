#include <filesystem>
#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include <unordered_map>
#include <string>
#include <cstdlib> 

#include "Util.h"
#include "MMap.h"
#include "CMSketch.h"

namespace fs = std::filesystem;

template<class T>
void ComputeFrequencyDistribution(const std::unordered_map<T, COUNT_TYPE>& record,
                                  const fs::path& outputFile) {
    std::vector<std::pair<T, COUNT_TYPE>> freqVector(record.begin(), record.end());
    std::sort(freqVector.begin(), freqVector.end(),
              [](auto const& a, auto const& b){ return a.second > b.second; });

    std::ofstream file(outputFile);
    if (!file) {
        std::cerr << "Error opening file: " << outputFile << "\n";
        return;
    }
    // Write CSV header
    file << "count" << "\n";
    for (auto const& p : freqVector)
        file << p.second << "\n";
    std::cout << "Saved: " << outputFile << "\n";
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0]
                  << " <MEMORY> <ALPHA> <dataset1> [dataset2 ...]\n";
        return 1;
    }

    // 1) Parse MEMORY and alpha
    uint32_t MEMORY = static_cast<uint32_t>(std::atoll(argv[1]));
    double alpha = std::atof(argv[2]);

    // Build filename prefix: threshold printed with 6 decimal places
    char buf[64];
    std::snprintf(buf, sizeof(buf), "memory_%u_threshold_%.6f", MEMORY, alpha);
    std::string prefix(buf);

    // 2) Process each dataset
    for (int idx = 3; idx < argc; ++idx) {
        fs::path inFile{ argv[idx] };
        fs::path stem = inFile.stem();
        fs::path outDir = fs::current_path() / stem;

        if (!fs::exists(outDir)) {
            if (!fs::create_directory(outDir)) {
                std::cerr << "Failed to create directory: " << outDir << "\n";
                continue;
            }
        }

        // Load data
        LoadResult result = Load(inFile.string().c_str());
        if (!result.start) {
            std::cerr << "Failed to load file: " << inFile << "\n";
            continue;
        }
        TUPLES* dataset = reinterpret_cast<TUPLES*>(result.start);
        uint64_t length = result.length / sizeof(TUPLES);

        // Count-Min Sketch & frequency maps
        std::unordered_map<TUPLES, COUNT_TYPE> flowFrequency, retainedFlowFrequency;
        CMSketch<TUPLES, COUNT_TYPE> sketch(MEMORY);
        COUNT_TYPE threshold = static_cast<COUNT_TYPE>(alpha * length);
        uint64_t RetainedCount = 0;

        for (uint64_t i = 0; i < length; ++i) {
            auto& key = dataset[i];
            flowFrequency[key]++;
            sketch.Insert(key);
            if (sketch.Query(key) >= threshold) {
                retainedFlowFrequency[key]++;
                RetainedCount++;
            }
        }

        // Log summary
        std::cout << "\n=== File: " << inFile << " ===\n"
                  << "Threshold: " << threshold << "\n"
                  << "Total Packets: " << length << "\n"
                  << "Flows Before Filter: " << flowFrequency.size() << "\n"
                  << "Packets After Filter: " << RetainedCount << "\n"
                  << "Flows After Filter: " << retainedFlowFrequency.size() << "\n";

        // Output frequency files as CSV
        ComputeFrequencyDistribution(
            flowFrequency,
            outDir / (prefix + "_all.csv")
        );
        ComputeFrequencyDistribution(
            retainedFlowFrequency,
            outDir / (prefix + "_retained.csv")
        );

        UnLoad(result);
    }

    return 0;
}
