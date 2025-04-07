#include <vector>
#include <fstream>

#include "Util.h"
#include "MMap.h"
#include "CMSketch.h"
#include <unordered_map>
#include <string.h>
#include <cstring>

template<class T>
void ComputeFrequencyDistribution(T &record, const std::string& outputFile) {
    std::vector<std::pair<TUPLES, COUNT_TYPE>> freqVector(record.begin(), record.end());

    std::sort(freqVector.begin(), freqVector.end(), [](const auto& a, const auto& b) {
        return a.second > b.second;
    });

    std::ofstream file(outputFile);
    if (!file.is_open()) {
        std::cerr << "Error opening file: " << outputFile << std::endl;
        return;
    }

    for (const auto& pair : freqVector) {
        file << pair.second << std::endl;
    }

    file.close();
    std::cout << "Frequency distribution saved to: " << outputFile << std::endl;
}

int main() {
    std::string filename = "equinix-chicago.dirA.20160121-140000.UTC.anon.dat"; 
    std::string PATH = "../../" + filename; 
    uint32_t MEMORY = 500000;
    double alpha = 0.0001;

    LoadResult result = Load(PATH.c_str());
    TUPLES* dataset = (TUPLES*)result.start;
    uint64_t length = result.length / sizeof(TUPLES);

    std::unordered_map<TUPLES, COUNT_TYPE> tuplesMpAll;
    std::unordered_map<TUPLES, COUNT_TYPE> tuplesMpAfterFilter;

    CMSketch<TUPLES, COUNT_TYPE>* sketch = new CMSketch<TUPLES, COUNT_TYPE>(MEMORY);

    COUNT_TYPE threshold = static_cast<COUNT_TYPE>(alpha * length);

    COUNT_TYPE lengthAfterFilter = 0;

    for (uint32_t i = 0; i < length; ++i) {
        tuplesMpAll[dataset[i]] += 1;
        sketch->Insert(dataset[i]);
        if (sketch->Query(dataset[i]) >= threshold) {
            tuplesMpAfterFilter[dataset[i]] += 1;
            lengthAfterFilter++;
        }
    }

    std::cout << "Threshold: " << threshold << std::endl;
    std::cout << "Number of Total Packets Before Filter: " << length << std::endl;
    std::cout << "Number of Total Flows: Before Filter " << tuplesMpAll.size() << std::endl;
    std::cout << "Number of Total Packets After Filter: " << lengthAfterFilter << std::endl;
    std::cout << "Number of Total Flows: After Filter " << tuplesMpAfterFilter.size() << std::endl;

    ComputeFrequencyDistribution(tuplesMpAll, "memory_" + std::to_string(MEMORY) + "_threshold_" + std::to_string(alpha) + "_all.txt");
    ComputeFrequencyDistribution(tuplesMpAfterFilter, "memory_" + std::to_string(MEMORY) + "_threshold_" + std::to_string(alpha) + "_filtered.txt");

    UnLoad(result);

    return 0;
}