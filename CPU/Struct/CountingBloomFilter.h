#ifndef COUNTINGBLOOMFILTER_H
#define COUNTINGBLOOMFILTER_H

#include "Util.h"
#include <vector>
#include <cstdint>
#include <algorithm>

template<typename DATA_TYPE, typename COUNT_TYPE>
class CountingBloomFilter {
public:
    std::string name = "CountingBloomFilter";

    CountingBloomFilter(uint32_t _MEMORY) {
        LENGTH = (_MEMORY * 8) / COUNTER_BIT; 
        filter.resize(LENGTH, 0);
    }

    ~CountingBloomFilter() = default;

    COUNT_TYPE Insert(const DATA_TYPE item) {
        return std::min(++filter[hash(item, 0) % LENGTH], ++filter[hash(item, 1) % LENGTH]);
    }

    COUNT_TYPE Query(const DATA_TYPE item) {
        return std::min(filter[hash(item, 0) % LENGTH], filter[hash(item, 1) % LENGTH]);
    }

private:
    std::vector<uint16_t> filter;
    uint32_t COUNTER_BIT = 16;
    const uint32_t HASH_NUM = 2;
    uint32_t LENGTH;
};

#endif
