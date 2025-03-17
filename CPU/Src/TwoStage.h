#ifndef TWOSTAGE_H
#define TWOSTAGE_H

#include "Abstract.h"
#include "Util.h"

#include "ColdFilter.h"
#include "CountingBloomFilter.h"
#include "CMSketch_SIMD.h"
#include "MVSketch.h"
#include "TwoFASketch.h"
#include "CocoSketch.h"
#include "UnivMon.h"
#include "Elastic.h"
#include "ElasticHeavyPart.h"
#include "CMHeap.h"
#include "CountHeap.h"
#include "SpaceSaving.h"
#include "StableSketch.h"
#include "MomentumSketch.h"
#include "MomentumSketch_SIMD.h"
#include "TightSketch.h"

#define Stage2SketchType MomentumSketch

template<typename DATA_TYPE>
class TwoStage : public Abstract<DATA_TYPE>{
public:
    typedef std::unordered_map<DATA_TYPE, COUNT_TYPE> HashMap;
    
    TwoStage(uint32_t _MEMORY, uint32_t _THRESHOLD){
        uint32_t FILTER_MEMORY = _MEMORY * FILTER_RATIO;
        uint32_t SKETCH_MEMORY = _MEMORY * SKETCH_RATIO;
        STAGE1_THRESHOLD = _THRESHOLD * STAGE1_TRESHOLD_RATIO;
        // STAGE2_THRESHOLD = _THRESHOLD * STAGE2_TRESHOLD_RATIO;

        // filter = new CountingBloomFilter<DATA_TYPE, uint16_t>(FILTER_MEMORY);
        // filter = new ColdFilter<DATA_TYPE, COUNT_TYPE>(FILTER_MEMORY, _THRESHOLD);
        filter = new CMSketch_SIMD<DATA_TYPE, uint16_t>(FILTER_MEMORY);

        sketch = new Stage2SketchType<DATA_TYPE>(SKETCH_MEMORY, STAGE1_THRESHOLD);

        this->name = "TwoStage ( " + filter->name + " + " + sketch->name + " )";
    }

    ~TwoStage(){
        delete filter;
        delete sketch;
    }

    void Insert(const DATA_TYPE& item){
        if (filter->Insert(item) >= STAGE1_THRESHOLD) {
            sketch->Insert(item);
        }
    }

    COUNT_TYPE Query(const DATA_TYPE& item){
        COUNT_TYPE temp = filter->Query(item);
        if (temp >= STAGE1_THRESHOLD) {
            return temp + sketch->Query(item);
        }
        return temp;
    }

    HashMap AllQuery(){
        return sketch->AllQuery();
    }
    
private:
    const double FILTER_RATIO = 0.5;
    const double SKETCH_RATIO = 0.5;

    COUNT_TYPE STAGE1_THRESHOLD;
    // COUNT_TYPE STAGE2_THRESHOLD;

    const double STAGE1_TRESHOLD_RATIO = 0.5;
    // const double STAGE2_TRESHOLD_RATIO = 0.2;

    CMSketch_SIMD<DATA_TYPE, uint16_t>* filter;
    Stage2SketchType<DATA_TYPE>* sketch;
};

#endif