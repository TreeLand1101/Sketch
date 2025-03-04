#ifndef TWOFASKETCH_H
#define TWOFASKETCH_H

#include "Abstract.h"
#include <limits> 

template<typename DATA_TYPE>
class TwoFASketch : public Abstract<DATA_TYPE> {
public:
    typedef std::unordered_map<DATA_TYPE, COUNT_TYPE> HashMap;
    static constexpr uint32_t COUNTER_PER_BUCKET = 8;

    struct Bucket{
        COUNT_TYPE vote;
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

    TwoFASketch(uint32_t _MEMORY, uint32_t _THRESHOLD = 3216, uint32_t _STAGE1_BIAS = 0, std::string _name = "TwoFASketch"){
        this->name = _name;

        this->stage1_bias = _STAGE1_BIAS;
        THRESHOLD = _THRESHOLD;
        LENGTH = _MEMORY / sizeof(Bucket);

        buckets = new Bucket[LENGTH];

        memset(buckets, 0, sizeof(Bucket) * LENGTH);
    }

    ~TwoFASketch(){
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

        if(minVal >= THRESHOLD / 2){
            pos = hash(item, 101) % LENGTH, minPos = 0;
            minVal = std::numeric_limits<COUNT_TYPE>::max();
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
            buckets[pos].vote += 1;
            if (buckets[pos].vote >= minVal) {
                buckets[pos].count[minPos] = buckets[pos].vote;
                buckets[pos].ID[minPos] = item;
                buckets[pos].vote = 0;
            }
        }
        else {
            buckets[pos].vote += 1;
            if (buckets[pos].vote >= minVal) {
                buckets[pos].count[minPos] = buckets[pos].vote;
                buckets[pos].ID[minPos] = item;
                buckets[pos].vote = 0;
            }
        }
    }

    COUNT_TYPE Query(const DATA_TYPE& item){
        return buckets[hash(item) % LENGTH].Query(item) + this->stage1_bias;
    }

    HashMap AllQuery(){
        HashMap ret;
        for(uint32_t i = 0;i < LENGTH;++i){
            for(uint32_t j = 0;j < COUNTER_PER_BUCKET;++j){
                if (buckets[i].ID[j][0] != '\0') {
                    ret[buckets[i].ID[j]] = buckets[i].count[j] + this->stage1_bias;
                }
            }
        }
        return ret;
    }

private:
    uint32_t LENGTH;
    uint32_t THRESHOLD;
    Bucket* buckets;
};

#endif