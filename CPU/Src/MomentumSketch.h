#ifndef MOMENTUMSKETCH_H
#define MOMENTUMSKETCH_H

#include "Abstract.h"
#include <bit>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <limits>

template<typename DATA_TYPE>
class MomentumSketch : public Abstract<DATA_TYPE> {
public:

    typedef std::unordered_map<DATA_TYPE, COUNT_TYPE> HashMap;

    struct Bucket{
        COUNT_TYPE momentum;
        DATA_TYPE ID;
        COUNT_TYPE counter;
    };

    MomentumSketch(uint32_t _MEMORY, uint32_t _STAGE1_BIAS = 0, std::string _name = "MomentumSketch"){
        this->name = _name;

        LENGTH = _MEMORY / sizeof(Bucket) / HASH_NUM;
        this->stage1_bias = _STAGE1_BIAS;
        sketch = new Bucket* [HASH_NUM];
        for(uint32_t i = 0; i < HASH_NUM; ++i){
            sketch[i] = new Bucket[LENGTH];
            memset(sketch[i], 0, sizeof(Bucket) * LENGTH);
        }
    }

    ~MomentumSketch(){
        for(uint32_t i = 0; i < HASH_NUM; ++i)
            delete [] sketch[i];
        delete [] sketch;
    }

    void Insert(const DATA_TYPE& item) {
        COUNT_TYPE min = std::numeric_limits<COUNT_TYPE>::max();
        int R = -1;
        int M = -1;

        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t pos = hash(item, i) % LENGTH;   
            // If bucket is empty, insert new item
            if (sketch[i][pos].ID[0] == '\0') {
                sketch[i][pos].ID = item;
                sketch[i][pos].counter = 1;
                sketch[i][pos].momentum = 1;
                return;
            }
            // If item already exists, update its momentum and counter
            if (item == sketch[i][pos].ID) {
                sketch[i][pos].momentum += sketch[i][pos].counter;
                if (sketch[i][pos].momentum < 0) {
                    sketch[i][pos].momentum = std::numeric_limits<COUNT_TYPE>::max();
                }
                sketch[i][pos].counter++;
                return;
            }
            // Keep track of bucket with minimum counter for potential replacement
            else if (sketch[i][pos].counter < min) {
                min = sketch[i][pos].counter;
                R = i;
                M = pos;
            }
        }

        // Decay the momentum of the bucket to be potentially replaced
        sketch[R][M].momentum /= 2;

        // Probabilistically replace the item based on counter and momentum
        if (rand() % (long long)(sketch[R][M].counter * sketch[R][M].momentum + 1) == 0) {
            // Decrement counter and if it reaches 0, replace with new item
            if (--sketch[R][M].counter == 0) {
                sketch[R][M].ID = item;
                sketch[R][M].counter = 1;
                sketch[R][M].momentum = 1;
            }
        }
    }

    COUNT_TYPE Query(const DATA_TYPE& item){
        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t pos = hash(item, i) % LENGTH;
            if (sketch[i][pos].ID == item) {
                return sketch[i][pos].counter;
            }
        }
        return 0;
    }

    HashMap AllQuery(){
        HashMap ret;

        for(uint32_t i = 0; i < HASH_NUM; ++i){
            for (uint32_t j = 0; j < LENGTH; ++j) {
                if (sketch[i][j].ID[0] != '\0' && ret.find(sketch[i][j].ID) == ret.end()) {
                    ret[sketch[i][j].ID] = Query(sketch[i][j].ID) + this->stage1_bias;
                }
            }
        }

        return ret;
    }

private:

    uint32_t LENGTH;
    const uint32_t HASH_NUM = 4;

    const uint32_t HH_THRESHOLD = 3216;
    const double HH_RATIO = 0.005;
    const uint32_t DECAY_CONST = HH_THRESHOLD * HH_RATIO;

    Bucket** sketch;
};

#endif