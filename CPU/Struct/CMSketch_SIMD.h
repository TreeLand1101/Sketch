#ifndef CMSKETCH_SIMD_H
#define CMSKETCH_SIMD_H

#include "Util.h"

template<typename DATA_TYPE,typename COUNT_TYPE>
class CMSketch_SIMD{
public:
    std::string name = "CMSketch_SIMD";   

    CMSketch_SIMD(uint32_t _MEMORY){
        LENGTH = _MEMORY / sizeof(COUNT_TYPE) / HASH_NUM;

        sketch = new COUNT_TYPE* [HASH_NUM];
        for(uint32_t i = 0;i < HASH_NUM; ++i){
            sketch[i] = new COUNT_TYPE[LENGTH];
            memset(sketch[i], 0, sizeof(COUNT_TYPE) * LENGTH);
        }
    }

    ~CMSketch_SIMD(){
        for(uint32_t i = 0;i < HASH_NUM;++i)
            delete [] sketch[i];
        delete [] sketch;
    }

    COUNT_TYPE Insert(const DATA_TYPE item) {
        COUNT_TYPE ret = std::numeric_limits<COUNT_TYPE>::max();

        __m128i hash_vec = hash_sse2(item);
        uint32_t hashes[4];
        _mm_store_si128(reinterpret_cast<__m128i*>(hashes), hash_vec);

        for (uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t position = hashes[i] % LENGTH;
            sketch[i][position] += 1;
            ret = MIN(ret, sketch[i][position]);
        }
        return ret;
    }

    COUNT_TYPE Query(const DATA_TYPE item){
        COUNT_TYPE ret = std::numeric_limits<COUNT_TYPE>::max();

        __m128i hash_vec = hash_sse2(item);
        uint32_t hashes[4];
        _mm_store_si128(reinterpret_cast<__m128i*>(hashes), hash_vec);

        for (uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t position = hashes[i] % LENGTH;
            ret = MIN(ret, sketch[i][position]);
        }

        return ret;
    }

private:
    uint32_t LENGTH;
    const uint32_t HASH_NUM = 4;
    uint32_t COUNTER_BIT = 16;
    COUNT_TYPE** sketch;
};

#endif
