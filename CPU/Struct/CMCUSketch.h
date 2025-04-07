#ifndef CMCUSKETCH_H
#define CMCUSKETCH_H

#include "Util.h"

template<typename DATA_TYPE,typename COUNT_TYPE>
class CMCUSketch{
public:
    std::string name = "CMCUSketch";   

    CMCUSketch(uint32_t _MEMORY, uint32_t _HASH_NUM = 4) {
        HASH_NUM = _HASH_NUM;
        name += " (row = " + std::to_string(_HASH_NUM) + ")";
        LENGTH = _MEMORY / sizeof(COUNT_TYPE) / HASH_NUM;
        index = new COUNT_TYPE [HASH_NUM];
        sketch = new COUNT_TYPE* [HASH_NUM];
        for(uint32_t i = 0;i < HASH_NUM; ++i){
            sketch[i] = new COUNT_TYPE[LENGTH];
            memset(sketch[i], 0, sizeof(COUNT_TYPE) * LENGTH);
        }
    }

    ~CMCUSketch(){
        for(uint32_t i = 0;i < HASH_NUM;++i)
            delete [] sketch[i];
        delete [] sketch;
        delete [] index;
    }

    COUNT_TYPE Insert(const DATA_TYPE& item) {
        COUNT_TYPE minVal = std::numeric_limits<COUNT_TYPE>::max();

        for (uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t position = hash(item, i) % LENGTH;
            index[i] = position;
            minVal = std::min(minVal, sketch[i][position]);
        }

        for (uint32_t i = 0; i < HASH_NUM; ++i) {
            if (sketch[i][index[i]] == minVal) {
                ++sketch[i][index[i]];
            }
        }

        return minVal + 1;
    }

    COUNT_TYPE Query(const DATA_TYPE& item){
        COUNT_TYPE ret = std::numeric_limits<COUNT_TYPE>::max();

        for (uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t position = hash(item, i) % LENGTH;
            ret = std::min(ret, sketch[i][position]);
        }

        return ret;
    }

private:
    uint32_t LENGTH;
    uint32_t HASH_NUM;
    uint32_t COUNTER_BIT = 16;
    COUNT_TYPE** sketch;
    COUNT_TYPE* index;
};

#endif
