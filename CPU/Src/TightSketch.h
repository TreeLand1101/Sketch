#ifndef TIGHTSKETCH_H
#define TIGHTSKETCH_H

#include "Abstract.h"
#include <limits>

template<typename DATA_TYPE>
class TightSketch : public Abstract<DATA_TYPE> {
public:

    typedef std::unordered_map<DATA_TYPE, COUNT_TYPE> HashMap;

    struct Bucket{
        COUNT_TYPE arrival_strength;
        DATA_TYPE ID;
        COUNT_TYPE counter;
    };

    TightSketch(uint32_t _MEMORY, uint32_t _STAGE1_BIAS = 0, std::string _name = "TightSketch"){
        this->name = _name;

        LENGTH = _MEMORY / sizeof(Bucket) / HASH_NUM;
        this->stage1_bias = _STAGE1_BIAS;
        sketch = new Bucket* [HASH_NUM];
        for(uint32_t i = 0; i < HASH_NUM; ++i){
            sketch[i] = new Bucket[LENGTH];
            memset(sketch[i], 0, sizeof(Bucket) * LENGTH);
        }
    }

    ~TightSketch(){
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
            if (sketch[i][pos].ID[0] == '\0') {
                sketch[i][pos].ID = item;
                sketch[i][pos].arrival_strength = 1;
                sketch[i][pos].counter = 1;
                return;
            }
            if (item == sketch[i][pos].ID) {
                sketch[i][pos].arrival_strength++;
                sketch[i][pos].counter++;
                return;
            }
            else if (sketch[i][pos].counter < min) {
                min = sketch[i][pos].counter;
                R = i;
                M = pos;
            }
            sketch[i][pos].arrival_strength = std::max(0, sketch[i][pos].arrival_strength - 1);
        }

        if (sketch[R][M].counter < DECAY_THRESHOLD) {
            if (rand() % (sketch[R][M].counter + 1) == 0) {
                sketch[R][M].counter--;
            }
        }
        else {
            if (rand() % (sketch[R][M].counter * sketch[R][M].arrival_strength + 1) == 0) {
                sketch[R][M].counter--;
            }
        }

        if (sketch[R][M].counter == 0) {
            sketch[R][M].ID = item;
            sketch[R][M].counter = 1;            
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

    const uint32_t DECAY_THRESHOLD = 10;

    Bucket** sketch;
};

#endif