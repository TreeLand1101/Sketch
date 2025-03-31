#ifndef CMCUSKETCH_H
#define CMCUSKETCH_H

#include "Util.h"

template<typename DATA_TYPE,typename COUNT_TYPE>
class CMCUSketch{
public:
    std::string name = "CMCUSketch";   

    CMCUSketch(uint32_t _MEMORY){
        LENGTH = _MEMORY / sizeof(COUNT_TYPE) / HASH_NUM;

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
    }

    COUNT_TYPE Insert(const DATA_TYPE item) {
        uint32_t i1 = hash(item, 0) % LENGTH;
        uint32_t i2 = hash(item, 1) % LENGTH;
        if (sketch[0][i1] < sketch[1][i2]) {
            return ++sketch[0][i1]; 
        }
        else if (sketch[0][i1] > sketch[1][i2]) {
            return ++sketch[1][i2]; 
        }

        ++sketch[0][i1]; 
        ++sketch[1][i2]; 
        return sketch[0][i1];
    }

    COUNT_TYPE Query(const DATA_TYPE item){
        COUNT_TYPE ret = std::numeric_limits<COUNT_TYPE>::max();

        for (uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t position = hash(item, i) % LENGTH;
            ret = MIN(ret, sketch[i][position]);
        }

        return ret;
    }

private:
    uint32_t LENGTH;
    const uint32_t HASH_NUM = 2;
    uint32_t COUNTER_BIT = 16;
    COUNT_TYPE** sketch;
};

#endif
