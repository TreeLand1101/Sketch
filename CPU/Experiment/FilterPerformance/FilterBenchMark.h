#include <arpa/inet.h> 
#include <netinet/in.h> 
#include <vector>
#include <fstream>

#include "MMap.h"

#include "CUSketch.h"
#include "CMSketch.h"

class FilterBenchMark{
public:

    FilterBenchMark(std::string PATH, std::string name){
        fileName = name;

        result = Load(PATH.c_str());
        dataset = (TUPLES*)result.start;
        length = result.length / sizeof(TUPLES);

        for(uint64_t i = 0; i < length; ++i){
            tuplesMp[dataset[i]] += 1;
        }
    }

    ~FilterBenchMark(){
        UnLoad(result);
    }

    template<typename Filter, typename... Args>
    void Bench(uint32_t MEMORY, Args&&... args) {
        Filter* tupleFilter = new Filter(MEMORY, std::forward<Args>(args)...);
    
        std::cout << "- " << tupleFilter->name << std::endl;
    
        Throughput(tupleFilter);
        Error(tupleFilter, tuplesMp);
    
        delete tupleFilter;
    }

private:
    std::string fileName;

    LoadResult result;

    TUPLES* dataset;
    uint64_t length;

    std::unordered_map<TUPLES, COUNT_TYPE> tuplesMp;

    template<class Filter, class T>
    void Error(Filter* tupleFilter, T& record) {
        double aae = 0, are = 0;
    
        for (auto it = record.begin(); it != record.end(); ++it) {
            double realF = it->second, estF = tupleFilter->Query(it->first);
            aae += abs(realF - estF);
            are += abs(realF - estF) / realF;
        }
    
        std::cout << "- Compare" << std::endl;
        std::cout << "    Total Packets: " << length << std::endl;
        std::cout << "    Total Flows: " << record.size() << std::endl;
        std::cout << "    AAE: " << aae / record.size() << std::endl;
        std::cout << "    ARE: " << are / record.size() << std::endl;
        std::cout << "+------------------------------------------------+" << std::endl;
    }
    

    template<class Filter>
    void Throughput(Filter* tupleFilter) {
        TP start, end;
        std::cout << "- Average Time Per Operation" << std::endl;

        start = std::chrono::high_resolution_clock::now();
        for (uint32_t j = 0; j < length; ++j) {
            tupleFilter->Insert(dataset[j]);
        }
        end = std::chrono::high_resolution_clock::now(); 
        std::cout << "    Insert: " << (durationms(end, start) / length) << " ms" << std::endl;

        start = std::chrono::high_resolution_clock::now();
        for (uint32_t j = 0; j < length; ++j) {
            tupleFilter->Query(dataset[j]);
        }
        end = std::chrono::high_resolution_clock::now(); 
        std::cout << "    Query: " << (durationms(end, start) / length) << " ms" << std::endl;
    }
};
