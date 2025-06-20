#ifndef MOMENTUMSKETCHVARIANT_H
#define MOMENTUMSKETCHVARIANT_H

#include "Abstract.h"
#include "MomentumSketch.h"
#include <bit>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <limits>

template<typename DATA_TYPE>
class Default : public MomentumSketch<DATA_TYPE> {
public:
    using MomentumSketch<DATA_TYPE>::LENGTH;
    using MomentumSketch<DATA_TYPE>::HASH_NUM;
    using MomentumSketch<DATA_TYPE>::sketch;

    Default(uint32_t _MEMORY, std::string _name = "Default") : MomentumSketch<DATA_TYPE>(_MEMORY, _name) {}
};

template<typename DATA_TYPE>
class Additive : public MomentumSketch<DATA_TYPE> {
public:
    using MomentumSketch<DATA_TYPE>::LENGTH;
    using MomentumSketch<DATA_TYPE>::HASH_NUM;
    using MomentumSketch<DATA_TYPE>::sketch;

    Additive(uint32_t _MEMORY, std::string _name = "Additive") : MomentumSketch<DATA_TYPE>(_MEMORY, _name) {}

    void Insert(const DATA_TYPE& item) {
        COUNT_TYPE min = std::numeric_limits<COUNT_TYPE>::max();
        int R = -1;
        int M = -1;

        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t pos = hash(item, i) % LENGTH;   
            if (sketch[i][pos].ID[0] == '\0') {
                sketch[i][pos].ID = item;
                sketch[i][pos].counter = 1;
                sketch[i][pos].momentum = 1;
                return;
            }
            if (item == sketch[i][pos].ID) {
                if (std::numeric_limits<COUNT_TYPE>::max() - sketch[i][pos].momentum < sketch[i][pos].counter) {
                    sketch[i][pos].momentum = std::numeric_limits<COUNT_TYPE>::max();
                } 
                else {
                    sketch[i][pos].momentum += sketch[i][pos].counter;
                }
                sketch[i][pos].counter++;
                return;
            }
            if (sketch[i][pos].counter < min) {
                min = sketch[i][pos].counter;
                R = i;
                M = pos;
            }
        }

        sketch[R][M].momentum /= 2;

        if (randomGenerator() % ((uint64_t)sketch[R][M].counter + sketch[R][M].momentum + 1) == 0) {
            if (--sketch[R][M].counter == 0) {
                sketch[R][M].ID = item;
                sketch[R][M].counter = 1;
                sketch[R][M].momentum = 1;
            }
        }
    }

};


template<typename DATA_TYPE>
class MomentumOnly : public MomentumSketch<DATA_TYPE> {
public:
    using MomentumSketch<DATA_TYPE>::LENGTH;
    using MomentumSketch<DATA_TYPE>::HASH_NUM;
    using MomentumSketch<DATA_TYPE>::sketch;

    MomentumOnly(uint32_t _MEMORY, std::string _name = "MomentumOnly") : MomentumSketch<DATA_TYPE>(_MEMORY, _name) {}

    void Insert(const DATA_TYPE& item) {
        COUNT_TYPE min = std::numeric_limits<COUNT_TYPE>::max();
        int R = -1;
        int M = -1;

        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t pos = hash(item, i) % LENGTH;   
            if (sketch[i][pos].ID[0] == '\0') {
                sketch[i][pos].ID = item;
                sketch[i][pos].counter = 1;
                sketch[i][pos].momentum = 1;
                return;
            }
            if (item == sketch[i][pos].ID) {
                if (std::numeric_limits<COUNT_TYPE>::max() - sketch[i][pos].momentum < sketch[i][pos].counter) {
                    sketch[i][pos].momentum = std::numeric_limits<COUNT_TYPE>::max();
                } 
                else {
                    sketch[i][pos].momentum += sketch[i][pos].counter;
                }
                sketch[i][pos].counter++;
                return;
            }
            if (sketch[i][pos].counter < min) {
                min = sketch[i][pos].counter;
                R = i;
                M = pos;
            }
        }

        sketch[R][M].momentum /= 2;

        if (randomGenerator() % ((uint64_t)sketch[R][M].momentum + 1) == 0) {
            if (--sketch[R][M].counter == 0) {
                sketch[R][M].ID = item;
                sketch[R][M].counter = 1;
                sketch[R][M].momentum = 1;
            }
        }
    }

};


template<typename DATA_TYPE>
class CounterOnly : public MomentumSketch<DATA_TYPE> {
public:
    using MomentumSketch<DATA_TYPE>::LENGTH;
    using MomentumSketch<DATA_TYPE>::HASH_NUM;
    using MomentumSketch<DATA_TYPE>::sketch;

    CounterOnly(uint32_t _MEMORY, std::string _name = "CounterOnly") : MomentumSketch<DATA_TYPE>(_MEMORY, _name) {}

    void Insert(const DATA_TYPE& item) {
        COUNT_TYPE min = std::numeric_limits<COUNT_TYPE>::max();
        int R = -1;
        int M = -1;

        for(uint32_t i = 0; i < HASH_NUM; ++i) {
            uint32_t pos = hash(item, i) % LENGTH;   
            if (sketch[i][pos].ID[0] == '\0') {
                sketch[i][pos].ID = item;
                sketch[i][pos].counter = 1;
                sketch[i][pos].momentum = 1;
                return;
            }
            if (item == sketch[i][pos].ID) {
                if (std::numeric_limits<COUNT_TYPE>::max() - sketch[i][pos].momentum < sketch[i][pos].counter) {
                    sketch[i][pos].momentum = std::numeric_limits<COUNT_TYPE>::max();
                } 
                else {
                    sketch[i][pos].momentum += sketch[i][pos].counter;
                }
                sketch[i][pos].counter++;
                return;
            }
            if (sketch[i][pos].counter < min) {
                min = sketch[i][pos].counter;
                R = i;
                M = pos;
            }
        }

        sketch[R][M].momentum /= 2;

        if (randomGenerator() % ((uint64_t)sketch[R][M].counter + 1) == 0) {
            if (--sketch[R][M].counter == 0) {
                sketch[R][M].ID = item;
                sketch[R][M].counter = 1;
                sketch[R][M].momentum = 1;
            }
        }
    }

};

#endif