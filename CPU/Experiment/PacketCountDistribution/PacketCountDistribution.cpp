#include <filesystem>
#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include <unordered_map>
#include <string>
#include <cstdlib>   // for std::atoll, std::atof

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
        std::unordered_map<TUPLES, COUNT_TYPE> flowFrequencyAll, flowFrequencyFiltered;
        CMSketch<TUPLES, COUNT_TYPE> sketch(MEMORY);
        COUNT_TYPE threshold = static_cast<COUNT_TYPE>(alpha * length);
        uint64_t countAfter = 0;

        for (uint64_t i = 0; i < length; ++i) {
            auto& key = dataset[i];
            flowFrequencyAll[key]++;
            sketch.Insert(key);
            if (sketch.Query(key) >= threshold) {
                flowFrequencyFiltered[key]++;
                countAfter++;
            }
        }

        // Log summary
        std::cout << "\n=== File: " << inFile << " ===\n"
                  << "Threshold: " << threshold << "\n"
                  << "Total Packets: " << length << "\n"
                  << "Flows Before Filter: " << flowFrequencyAll.size() << "\n"
                  << "Packets After Filter: " << countAfter << "\n"
                  << "Flows After Filter: " << flowFrequencyFiltered.size() << "\n";

        // Output frequency files
        ComputeFrequencyDistribution(
            flowFrequencyAll,
            outDir / (prefix + "_all.txt")
        );
        ComputeFrequencyDistribution(
            flowFrequencyFiltered,
            outDir / (prefix + "_filtered.txt")
        );

        UnLoad(result);
    }

    return 0;
}
