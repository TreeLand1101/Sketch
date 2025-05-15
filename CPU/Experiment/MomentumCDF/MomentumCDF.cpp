#include <arpa/inet.h>
#include <netinet/in.h>
#include <vector>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <algorithm>
#include <limits>
#include <iomanip>
#include "MMap.h"
#include "Abstract.h"

template<typename DATA_TYPE>
class MVSketch_MomentumCDF : public Abstract<DATA_TYPE> {
public:

    typedef std::unordered_map<DATA_TYPE, COUNT_TYPE> HashMap;

    struct Bucket{
        COUNT_TYPE total_sum;
        DATA_TYPE ID;
        COUNT_TYPE counter;
    };

    MVSketch_MomentumCDF(uint32_t _MEMORY, std::string _name = "MVSketch_MomentumCDF"){
        this->name = _name;

        LENGTH = _MEMORY / sizeof(Bucket) / HASH_NUM;
        sketch = new Bucket* [HASH_NUM];
        for(uint32_t i = 0; i < HASH_NUM; ++i){
            sketch[i] = new Bucket[LENGTH];
            memset(sketch[i], 0, sizeof(Bucket) * LENGTH);
        }
    }

    ~MVSketch_MomentumCDF(){
        for(uint32_t i = 0; i < HASH_NUM; ++i)
            delete [] sketch[i];
        delete [] sketch;
    }

    void Insert(const DATA_TYPE& item) {
        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t pos = hash(item, i) % LENGTH;
            sketch[i][pos].total_sum++;
            if (sketch[i][pos].ID[0] == '\0') {
                sketch[i][pos].ID = item;
                sketch[i][pos].counter = 1;
            }
            else if (item == sketch[i][pos].ID) {
                sketch[i][pos].counter++;
            }
            else {
                if (sketch[i][pos].counter == 0) {
                    sketch[i][pos].ID = item;
                    sketch[i][pos].counter = 1;
                }
                else {
                    --sketch[i][pos].counter;
                }
            }
        }
    }

    COUNT_TYPE Query(const DATA_TYPE& item) {
        COUNT_TYPE ret = std::numeric_limits<COUNT_TYPE>::max();

        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t pos = hash(item, i) % LENGTH;
            if (sketch[i][pos].ID == item) {
                ret = std::min(ret, (sketch[i][pos].total_sum + sketch[i][pos].counter) / 2);
            }
            else {
                ret = std::min(ret, (sketch[i][pos].total_sum - sketch[i][pos].counter) / 2);
            }
        }

        return ret;
    }

    HashMap AllQuery() {
        HashMap ret;

        for(uint32_t i = 0; i < HASH_NUM; ++i){
            for (uint32_t j = 0; j < LENGTH; ++j) {
                if (sketch[i][j].ID[0] != '\0' && ret.find(sketch[i][j].ID) == ret.end()) {
                    ret[sketch[i][j].ID] = Query(sketch[i][j].ID);
                }
            }
        }

        return ret;
    }

    bool Search(const DATA_TYPE& item) {
        for (uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t pos = hash(item, i) % LENGTH;
            if (sketch[i][pos].ID == item) {
                return true;
            }
        }
        return false;
    }

private:
    uint32_t LENGTH;
    const uint32_t HASH_NUM = 4;
    Bucket** sketch;
};

int main() {
    std::string PATH = "../../equinix-chicago.dirA.20160121-140000.UTC.anon.dat";
    uint32_t MEMORY = 500000;
    double alpha = 0.0001;
    COUNT_TYPE maxMomentum = 1e8;

    LoadResult result = Load(PATH.c_str());
    TUPLES* dataset = (TUPLES*)result.start;
    uint64_t length = result.length / sizeof(TUPLES);

    std::unordered_map<TUPLES, COUNT_TYPE> tuplesMp;
    std::unordered_map<TUPLES, COUNT_TYPE> tuplesMomentum;

    MVSketch_MomentumCDF<TUPLES>* sketch = new MVSketch_MomentumCDF<TUPLES>(MEMORY);

    for (uint64_t i = 0; i < length; ++i) {
        TUPLES flow = dataset[i];
        tuplesMp[flow] += 1;
        if (tuplesMomentum.find(flow) == tuplesMomentum.end()) {
            tuplesMomentum[flow] = 0;
        }
        if (sketch->Search(flow)) {
            tuplesMomentum[flow] += sketch->Query(flow);
            if (tuplesMomentum[flow] > maxMomentum) {
                tuplesMomentum[flow] = maxMomentum;
            }
        } else {
            tuplesMomentum[flow] = tuplesMomentum[flow] / 2;
        }
        sketch->Insert(flow);
    }

    COUNT_TYPE threshold = static_cast<COUNT_TYPE>(alpha * length);

    std::vector<COUNT_TYPE> nonHeavyMomentum;
    std::vector<COUNT_TYPE> heavyHitterMomentum;

    for (const auto& pair : tuplesMp) {
        const TUPLES& flow = pair.first;
        COUNT_TYPE count = pair.second;
        COUNT_TYPE momentum = tuplesMomentum[flow];
        if (count >= threshold) {
            heavyHitterMomentum.push_back(momentum);
        } else {
            nonHeavyMomentum.push_back(momentum);
        }
    }

    std::sort(nonHeavyMomentum.begin(), nonHeavyMomentum.end());
    std::sort(heavyHitterMomentum.begin(), heavyHitterMomentum.end());

    std::string nonHeavyCSV = "nonheavy_momentum_cdf.csv";
    std::string heavyHitterCSV = "heavyhitter_momentum_cdf.csv";
    std::ofstream nonHeavyOut(nonHeavyCSV);
    std::ofstream heavyHitterOut(heavyHitterCSV);

    nonHeavyOut << "momentum,cdf" << std::endl;
    heavyHitterOut << "momentum,cdf" << std::endl;

    nonHeavyOut << std::fixed << std::setprecision(6);
    heavyHitterOut << std::fixed << std::setprecision(6);

    if (!nonHeavyMomentum.empty()) {
        for (size_t i = 0; i < nonHeavyMomentum.size(); ++i) {
            double cdf = static_cast<double>(i + 1) / nonHeavyMomentum.size();
            nonHeavyOut << nonHeavyMomentum[i] << "," << cdf << std::endl;
        }
    } else {
        nonHeavyOut << "0,0" << std::endl;
    }

    if (!heavyHitterMomentum.empty()) {
        for (size_t i = 0; i < heavyHitterMomentum.size(); ++i) {
            double cdf = static_cast<double>(i + 1) / heavyHitterMomentum.size();
            heavyHitterOut << heavyHitterMomentum[i] << "," << cdf << std::endl;
        }
    } else {
        heavyHitterOut << "0,0" << std::endl;
    }

    nonHeavyOut.close();
    heavyHitterOut.close();

    UnLoad(result);
    delete sketch;

    return 0;
}
