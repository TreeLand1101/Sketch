#ifndef CBFCU_H
#define CBFCU_H

#include "Util.h"
#include <cstdint>
#include <algorithm>

template<typename DATA_TYPE, typename COUNT_TYPE>
class CBFCU {
public:
    std::string name = "CBFCU";

    CBFCU(uint32_t _MEMORY, uint32_t _HASH_NUM = 2) {
        HASH_NUM = _HASH_NUM;
        name += " (row = " + std::to_string(_HASH_NUM) + ")";
        LENGTH = _MEMORY / sizeof(COUNT_TYPE); 
        filter = new COUNT_TYPE[LENGTH];
        index = new COUNT_TYPE[HASH_NUM];
        memset(filter, 0, sizeof(COUNT_TYPE) * LENGTH);
    }

    ~CBFCU() {
        delete [] filter;
        delete [] index;
    }

    COUNT_TYPE Insert(const DATA_TYPE& item) {
        COUNT_TYPE minVal = std::numeric_limits<COUNT_TYPE>::max();

        for (uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t position = hash(item, i) % LENGTH;
            index[i] = position;
            minVal = std::min(minVal, filter[position]);
        }

        for (uint32_t i = 0; i < HASH_NUM; ++i) {
            if (filter[index[i]] == minVal) {
                ++filter[index[i]];
            }
        }

        return minVal + 1;
    }

    COUNT_TYPE Query(const DATA_TYPE& item) {
        COUNT_TYPE ret = std::numeric_limits<COUNT_TYPE>::max();

        for (uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t position = hash(item, i) % LENGTH;
            ret = std::min(ret, filter[position]);
        }

        return ret;
    }

private:
    uint32_t COUNTER_BIT = 16;
    uint32_t HASH_NUM;
    uint32_t LENGTH;

    COUNT_TYPE* filter;
    COUNT_TYPE* index;
};

#endif
