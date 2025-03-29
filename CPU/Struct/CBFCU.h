#ifndef CBFCU_H
#define CBFCU_H

#include "Util.h"
#include <cstdint>
#include <algorithm>

template<typename DATA_TYPE, typename COUNT_TYPE>
class CBFCU {
public:
    std::string name = "CBFCU";

    CBFCU(uint32_t _MEMORY) {
        LENGTH = _MEMORY / sizeof(COUNT_TYPE); 
        filter = new COUNT_TYPE[LENGTH];
        memset(filter, 0, sizeof(COUNT_TYPE) * LENGTH);
    }

    ~CBFCU() {
        delete [] filter;
    }

    COUNT_TYPE Insert(const DATA_TYPE item) {
        uint32_t i1 = hash(item, 0) % LENGTH;
        uint32_t i2 = hash(item, 1) % LENGTH;
        if (filter[i1] < filter[i2]) {
            return ++filter[i1]; 
        }
        else if (filter[i1] > filter[i2]) {
            return ++filter[i2]; 
        }

        ++filter[i1];
        ++filter[i2];
        return filter[i1];
    }

    COUNT_TYPE Query(const DATA_TYPE item) {
        return std::min(filter[hash(item, 0) % LENGTH], filter[hash(item, 1) % LENGTH]);
    }

private:
    uint32_t COUNTER_BIT = 16;
    const uint32_t HASH_NUM = 2;
    uint32_t LENGTH;

    COUNT_TYPE* filter;
};

#endif
