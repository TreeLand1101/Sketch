#ifndef HHBENCH_H
#define HHBENCH_H

#include <arpa/inet.h> 
#include <netinet/in.h> 
#include <vector>
#include <fstream>

#include "MMap.h"
#include "CocoSketch.h"
#include "UnivMon.h"
#include "Elastic.h"
#include "CMHeap.h"
#include "CountHeap.h"
#include "SpaceSaving.h"
#include "MVSketch.h"
#include "StableSketch.h"
#include "Proposed.h"

class BenchMark{
public:

    BenchMark(std::string PATH, std::string name){
        fileName = name;

        result = Load(PATH.c_str());
        dataset = (TUPLES*)result.start;
        length = result.length / sizeof(TUPLES);

        for(uint64_t i = 0; i < length; ++i){
            tuplesMp[dataset[i]] += 1;
        }
    }

    ~BenchMark(){
        UnLoad(result);
    }

    void HHBench(uint32_t MEMORY, double alpha) {

        Abstract<TUPLES>* tupleSketch;

        COUNT_TYPE threshold = alpha * length;

        /* Modify SketchType to run on difference sketch */ 

        /* Proposed */
        // #define SketchType Proposed
        // tupleSketch = new SketchType<TUPLES>(MEMORY, threshold);

        /* Other */
        #define SketchType Elastic
        tupleSketch = new SketchType<TUPLES>(MEMORY);


        std::cout << "+--------------------------------------------+" << std::endl;
        std::cout << "- " << tupleSketch->name << std::endl;

        Throughput(tupleSketch);

        std::unordered_map<TUPLES, COUNT_TYPE> estTuple = tupleSketch->AllQuery();

        CompareHH(estTuple, tuplesMp, threshold, alpha);
        std::cout << "+--------------------------------------------+" << std::endl;
        // printTopK(estTuple, 10000);
        // printTopK(tuplesMp, 10);

        delete tupleSketch;
    }

private:
    std::string fileName;

    LoadResult result;

    TUPLES* dataset;
    uint64_t length;

    std::unordered_map<TUPLES, COUNT_TYPE> tuplesMp;

    template<class T>
    void CompareHH(T mp, T record, COUNT_TYPE threshold, double alpha){
        double realHH = 0, estHH = 0, bothHH = 0, aae = 0, are = 0;

        for(auto it = record.begin(); it != record.end(); ++it){
            bool real, est;
            double realF = it->second, estF = mp[it->first];
            
            real = (realF > threshold);
            est = (estF > threshold);

            realHH += real;
            estHH += est;

            if(real && est){
                bothHH += 1;
                aae += abs(realF - estF);
                are += abs(realF - estF) / realF;
            }
        }

        double recall = bothHH / realHH;
        double precision = bothHH / estHH;
        double f1score = 2 * (precision * recall) / (precision + recall);

        std::cout << "- CompareHH" << std::endl;
        std::cout << "    Total Packets: " << length << std::endl;
        std::cout << "    Threshold: " << std::fixed << alpha * 100 << "% (Packet Count: "<< threshold << ")" << std::endl;
        std::cout << "    Recall: " << recall << std::endl;
        std::cout << "    Precision: " << precision << std::endl;
        std::cout << "    F1 Socre: " <<  f1score << std::endl;        
        std::cout << "    AAE: " << aae / bothHH << std::endl;
        std::cout << "    ARE: " << are / bothHH << std::endl;
    }

    template<class T>
    void Throughput(T& tupleSketch) {
        TP start, end;
        std::cout << "- Average Time Per Operation" << std::endl;

        start = std::chrono::high_resolution_clock::now();
        for (uint32_t j = 0; j < length; ++j) {
            tupleSketch->Insert(dataset[j]);
        }
        end = std::chrono::high_resolution_clock::now(); 
        std::cout << "    Insert: " << (durationms(end, start) / length) << " ms" << std::endl;

        start = std::chrono::high_resolution_clock::now();
        for (uint32_t j = 0; j < length; ++j) {
            tupleSketch->Query(dataset[j]);
        }
        end = std::chrono::high_resolution_clock::now(); 
        std::cout << "    Query: " << (durationms(end, start) / length) << " ms" << std::endl;
    }


    // Print the top K most frequent TUPLES
    template<class T>
    void printTopK(T& M, int K) {
        auto ipToString = [](uint32_t ip) -> std::string {
            struct in_addr addr;
            addr.s_addr = ip;
            return inet_ntoa(addr);
        };

        std::vector<std::pair<TUPLES, COUNT_TYPE>> vec(M.begin(), M.end());

        std::sort(vec.begin(), vec.end(), [](const auto& a, const auto& b) {
            return a.second > b.second; 
        });
        std::cout << "Top " << K << " TUPLES:\n";
        int count = 0;
        for (const auto& entry : vec) { 
            if (count++ >= K) break; 

            const TUPLES& tuple = entry.first;
            COUNT_TYPE freq = entry.second;

            std::cout << "FLow: " << ipToString(tuple.srcIP()) << " / "
                    << ipToString(tuple.dstIP()) << " / "
                    << ntohs(tuple.srcPort()) << " / "
                    << ntohs(tuple.dstPort()) << " / "
                    << static_cast<int>(tuple.proto()) << " : "
                    << "Freq: " << freq << "\n";
        }
    }
};

#endif
