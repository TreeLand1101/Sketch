#ifndef CMSKETCH_H
#define CMSKETCH_H

#include "Util.h"

template<typename DATA_TYPE,typename COUNT_TYPE>
class CMSketch{
public:
    std::string name = "CMSketch";

    CMSketch(uint32_t _MEMORY, uint32_t _HASH_NUM = 4) {
        HASH_NUM = _HASH_NUM;
        name += " (row = " + std::to_string(_HASH_NUM) + ")";
        LENGTH = _MEMORY / sizeof(COUNT_TYPE) / HASH_NUM;

        sketch = new COUNT_TYPE* [HASH_NUM];
        for(uint32_t i = 0;i < HASH_NUM; ++i){
            sketch[i] = new COUNT_TYPE[LENGTH];
            memset(sketch[i], 0, sizeof(COUNT_TYPE) * LENGTH);
        }
    }

    ~CMSketch(){
        for(uint32_t i = 0;i < HASH_NUM;++i)
            delete [] sketch[i];
        delete [] sketch;
    }

    COUNT_TYPE Insert(const DATA_TYPE& item) {
        COUNT_TYPE ret = std::numeric_limits<COUNT_TYPE>::max();

        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t position = hash(item, i) % LENGTH;
            sketch[i][position] += 1;
            ret = std::min(ret, sketch[i][position]);
        }

        return ret;
    }

    COUNT_TYPE Query(const DATA_TYPE& item){
        COUNT_TYPE ret = std::numeric_limits<COUNT_TYPE>::max();

        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t position = hash(item, i) % LENGTH;
            ret = std::min(ret, sketch[i][position]);
        }

        return ret;
    }

private:
    uint32_t LENGTH;
    uint32_t HASH_NUM;

    COUNT_TYPE** sketch;
};

#endif
