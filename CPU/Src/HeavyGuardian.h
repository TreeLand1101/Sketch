#ifndef HEAVYGUARDIAN_H
#define HEAVYGUARDIAN_H

#include "Abstract.h"
#include <limits> 

template<typename DATA_TYPE>
class HeavyGuardian : public Abstract<DATA_TYPE> {
public:
    typedef std::unordered_map<DATA_TYPE, COUNT_TYPE> HashMap;
    static constexpr uint32_t COUNTER_PER_BUCKET = 8;

    struct Bucket{
        DATA_TYPE ID[COUNTER_PER_BUCKET];
        COUNT_TYPE count[COUNTER_PER_BUCKET];

        COUNT_TYPE Query(const DATA_TYPE item) {
            for(uint32_t i = 0; i < COUNTER_PER_BUCKET; i++) {
                if(ID[i] == item) {
                    return count[i];
                }
            }
            return 0;
        }
    };

    HeavyGuardian(uint32_t _MEMORY, uint32_t _STAGE1_BIAS = 0, std::string _name = "HeavyGuardian"){
        this->name = _name;

        this->stage1_bias = _STAGE1_BIAS;
        LENGTH = _MEMORY / sizeof(Bucket);

        buckets = new Bucket[LENGTH];

        memset(buckets, 0, sizeof(Bucket) * LENGTH);
    }

    ~HeavyGuardian(){
        delete [] buckets;
    }

    void Insert(const DATA_TYPE& item) {
        uint32_t pos = hash(item) % LENGTH, minPos = 0;
        COUNT_TYPE minVal = std::numeric_limits<COUNT_TYPE>::max();

        for (uint32_t i = 0; i < COUNTER_PER_BUCKET; i++){
            if(buckets[pos].ID[i] == item){
                buckets[pos].count[i] += 1;
                return;
            }

            if(buckets[pos].count[i] == 0){
                buckets[pos].ID[i] = item;
                buckets[pos].count[i] = 1;
                return;
            }

            if(buckets[pos].count[i] < minVal){
                minPos = i;
                minVal = buckets[pos].count[i];
            }
        }

        if (randomGenerator() % (int)(std::pow(decrementBase, buckets[pos].count[minPos])) == 0) {
            if (--buckets[pos].count[minPos] <= 0) {
                buckets[pos].ID[minPos] = item;
                buckets[pos].count[minPos] = 1;                
            }
        }
    }

    COUNT_TYPE Query(const DATA_TYPE& item){
        return buckets[hash(item) % LENGTH].Query(item);
    }

    HashMap AllQuery(){
        HashMap ret;
        for(uint32_t i = 0; i < LENGTH; ++i){
            for(uint32_t j = 0; j < COUNTER_PER_BUCKET; ++j) {
                if (buckets[i].ID[j][0] != '\0') {
                    ret[buckets[i].ID[j]] = buckets[i].count[j] + this->stage1_bias;
                }
            }
        }
        return ret;
    }

private:
    uint32_t LENGTH;
    Bucket* buckets;
    const double decrementBase = 1.08;
};

#endif