#ifndef CUCBF_H
#define CUCBF_H

#include "Util.h"
#include <cstdint>
#include <algorithm>

template<typename DATA_TYPE, typename COUNT_TYPE>
class CUCBF {
public:
    std::string name = "CUCBF";

    CUCBF(uint32_t _MEMORY, uint32_t _HASH_NUM = 2) {
        HASH_NUM = _HASH_NUM;
        LENGTH = _MEMORY / sizeof(COUNT_TYPE); 
        filter = new COUNT_TYPE[LENGTH];
        index = new uint32_t[HASH_NUM];
        memset(filter, 0, sizeof(COUNT_TYPE) * LENGTH);
    }

    ~CUCBF() {
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

        COUNT_TYPE ret = minVal + 1;

        for (uint32_t i = 0; i < HASH_NUM; ++i) {
            filter[index[i]] = std::max(filter[index[i]], ret);
        }

        return ret;
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
    uint32_t HASH_NUM;
    uint32_t LENGTH;

    COUNT_TYPE* filter;
    uint32_t* index;
};

#endif
