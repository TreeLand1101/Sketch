#ifndef COLDFILTER_H
#define COLDFILTER_H

#include "Util.h"
#include <vector>
#include <cstdint>
#include <algorithm>

template<typename DATA_TYPE, typename COUNT_TYPE>
class ColdFilter {
public:
    ColdFilter(uint32_t _MEMORY, uint32_t _THRESHOLD) {

        uint32_t layer1_length = (_MEMORY * L1_MEMORY_RATIO * 8) / L1_COUNTER_BIT; 
        layer1.resize(layer1_length, 0);

        uint32_t layer2_length = (_MEMORY * L2_MEMORY_RATIO * 8) / L2_COUNTER_BIT; 
        layer2.resize(layer2_length, 0);

        // uint32_t layer3_length = (_MEMORY * L3_MEMORY_RATIO * 8) / 32;
        // layer3.resize(layer3_length, 0);

        uint32_t layer1_max_count = (1 << L1_COUNTER_BIT) - 1; 
        uint32_t layer2_max_count = (1 << L2_COUNTER_BIT) - 1;
        // uint32_t layer3_max_count = (1 << L3_COUNTER_BIT) - 1;

        if (layer1_max_count + layer2_max_count /*+ layer3_max_count*/ < _THRESHOLD) {
            throw std::invalid_argument("Threshold is too large: exceeds the total capacity of all layers.");
        }

        if (layer1_max_count >= _THRESHOLD) {
            throw std::invalid_argument("Threshold is too small: the threshold of layer 2 is 0.");
        }

        // if (layer1_max_count + layer2_max_count >= _THRESHOLD) {
        //     throw std::invalid_argument("Threshold is too small: the threshold of layer 3 is 0.");
        // }

        thresholds.push_back(layer1_max_count);
        thresholds.push_back(_THRESHOLD - layer1_max_count);
        // thresholds.push_back(_THRESHOLD - layer1_max_count - layer2_max_count);

        // for (auto& t:thresholds) {
        //     std::cout << t << std::endl;
        // }
    }

    ~ColdFilter() = default;

    COUNT_TYPE Insert(const DATA_TYPE item) {
        COUNT_TYPE ret = 0;

        ret += processLayer(item, layer1, thresholds[0]);

        if (ret == thresholds[0]) {
            ret += processLayer(item, layer2, thresholds[1]);
        }

        // if (ret == thresholds[0] + thresholds[1]) {
        //     ret += processLayer(item, layer3, thresholds[2]);
        // }

        return ret;
    }

    COUNT_TYPE Query(const DATA_TYPE item) {
        COUNT_TYPE ret = 0;

        ret += queryLayer(item, layer1, thresholds[0]);

        if (ret == thresholds[0]) {
            ret += queryLayer(item, layer2, thresholds[1]);
        }

        // if (ret == thresholds[0] + thresholds[1]) {
        //     ret += queryLayer(item, layer3, thresholds[2]);
        // }

        return ret;
    }

private:
    std::vector<uint8_t> layer1;
    std::vector<uint16_t> layer2;
    // std::vector<uint16_t> layer3;

    std::vector<uint32_t> thresholds;
    const uint32_t HASH_NUM = 2;
    const uint32_t L1_COUNTER_BIT = 8;
    const uint32_t L2_COUNTER_BIT = 16;
    // const uint32_t L3_COUNTER_BIT = 16;

    const double L1_MEMORY_RATIO = 0.6;
    const double L2_MEMORY_RATIO = 0.4;
    // const double L3_MEMORY_RATIO = 0.2;

    template<typename LAYER_TYPE>
    COUNT_TYPE processLayer(const DATA_TYPE& item, std::vector<LAYER_TYPE>& layer, uint32_t& layer_threshold) {
        uint32_t layer_size = layer.size();
        uint32_t min_count = layer_threshold;

        for (int j = 0; j < HASH_NUM; ++j) {
            uint32_t pos = hash(item, j) % layer_size;
            min_count = std::min(min_count, static_cast<uint32_t>(layer[pos]));
        }

        if (min_count < layer_threshold) {
            for (int j = 0; j < HASH_NUM; ++j) {
                uint32_t pos = hash(item, j) % layer_size;
                if (layer[pos] < layer_threshold) {
                    layer[pos]++;
                }
            }
            return min_count + 1;
        }

        return layer_threshold;
    }

    template<typename LAYER_TYPE>
    COUNT_TYPE queryLayer(const DATA_TYPE& item, const std::vector<LAYER_TYPE>& layer, uint32_t layer_threshold) {
        uint32_t layer_size = layer.size();
        uint32_t min_count = layer_threshold;

        for (int j = 0; j < HASH_NUM; ++j) {
            uint32_t pos = hash(item, j) % layer_size;
            min_count = std::min(min_count, static_cast<uint32_t>(layer[pos]));
        }

        return min_count;
    }
};

#endif
