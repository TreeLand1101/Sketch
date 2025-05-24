#ifndef MOMENTUMSKETCHSIMD_H
#define MOMENTUMSKETCHSIMD_H

#include "Abstract.h"
#include <bit>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <limits>
#include <omp.h>
#include <immintrin.h>

#define TUPLES_LEN 13

struct TUPLES {
    uint8_t data[TUPLES_LEN];

    inline uint32_t srcIP() const {
        return *((uint32_t*)(data));
    }

    inline uint32_t dstIP() const {
        return *((uint32_t*)(&data[4]));
    }

    inline uint16_t srcPort() const {
        return *((uint16_t*)(&data[8]));
    }

    inline uint16_t dstPort() const {
        return *((uint16_t*)(&data[10]));
    }

    inline uint8_t proto() const {
        return *((uint8_t*)(&data[12]));
    }

    uint8_t& operator[](size_t index) {
        return data[index];
    }

    inline uint64_t srcIP_dstIP() const {
        return *((uint64_t*)(data));
    }
};

bool operator==(const TUPLES& a, const TUPLES& b) {
    return memcmp(a.data, b.data, sizeof(TUPLES)) == 0;
}

template<typename DATA_TYPE>
class MomentumSketchSIMD : public Abstract<DATA_TYPE> {
public:
    typedef std::unordered_map<DATA_TYPE, COUNT_TYPE> HashMap;

    struct Bucket {
        COUNT_TYPE momentum;
        DATA_TYPE ID;
        COUNT_TYPE counter;
    };

    MomentumSketchSIMD(uint32_t _MEMORY, std::string _name = "MomentumSketchSIMD") {
        this->name = _name;

        LENGTH = _MEMORY / sizeof(Bucket) / HASH_NUM;
        sketch = new Bucket* [HASH_NUM];
        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            sketch[i] = new Bucket[LENGTH];
            memset(sketch[i], 0, sizeof(Bucket) * LENGTH);
        }
    }

    ~MomentumSketchSIMD() {
        for(uint32_t i = 0; i < HASH_NUM; ++i)
            delete [] sketch[i];
        delete [] sketch;
    }

    __m128i to_m128i(const DATA_TYPE& item) {
        alignas(16) uint8_t buffer[16] = {0};
        memcpy(buffer, item.data, TUPLES_LEN);
        return _mm_load_si128(reinterpret_cast<__m128i*>(buffer));
    }

    void Insert(const DATA_TYPE& item) {
        COUNT_TYPE min = std::numeric_limits<COUNT_TYPE>::max();
        int R = -1, M = -1;

        uint32_t onehash[4];
        hash128(item, onehash);

        Bucket* sbucket[4];
        for(int i = 0; i < HASH_NUM; ++i) {
            uint32_t bucket = onehash[i] % LENGTH;
            sbucket[i] = &sketch[i][bucket];
        }

        __m512i vkey = _mm512_set_epi128(
            to_m128i(sbucket[3]->ID),
            to_m128i(sbucket[2]->ID),
            to_m128i(sbucket[1]->ID),
            to_m128i(sbucket[0]->ID)
        );

        __m128i item_m128i = to_m128i(item);
        __m512i comkey = _mm512_set1_epi128(item_m128i);

        __mmask16 mask = _mm512_cmpeq_epi128_mask(vkey, comkey);

        for (int i = 0; i < 4; ++i) {
            if (mask & (1 << i)) {
                sbucket[i]->momentum += sbucket[i]->counter;
                if (sbucket[i]->momentum < 0)
                    sbucket[i]->momentum = std::numeric_limits<COUNT_TYPE>::max();
                sbucket[i]->counter++;
                return;
            }
        }

        for(int i = 0; i < HASH_NUM; ++i) {
            if(sbucket[i]->ID[0] == '\0') {
                sbucket[i]->ID = item;
                sbucket[i]->counter = 1;
                sbucket[i]->momentum = 1;
                return;
            }
            if(sbucket[i]->counter < min) {
                min = sbucket[i]->counter;
                R = i;
                M = onehash[i] % LENGTH;
            }
        }

        sketch[R][M].momentum /= 2;
        if(randomGenerator() % (uint64_t)(sketch[R][M].counter * sketch[R][M].momentum + 1) == 0) {
            if(--sketch[R][M].counter == 0) {
                sketch[R][M].ID = item;
                sketch[R][M].counter = 1;
                sketch[R][M].momentum = 1;
            }
        }
    }

    COUNT_TYPE Query(const DATA_TYPE& item) {
        uint32_t onehash[4];
        hash128(item, onehash);

        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t bucket = onehash[i] % LENGTH;
            Bucket* b = &sketch[i][bucket];
            if(b->ID == item) return b->counter;
        }
        return 0;
    }

    HashMap AllQuery() {
        HashMap ret;

        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            for (uint32_t j = 0; j < LENGTH; ++j) {
                if (sketch[i][j].ID[0] != '\0' && ret.find(sketch[i][j].ID) == ret.end()) {
                    ret[sketch[i][j].ID] = Query(sketch[i][j].ID);
                }
            }
        }

        return ret;
    }

private:
    uint32_t LENGTH;
    const uint32_t HASH_NUM = 4;

    Bucket** sketch;
};

#endif