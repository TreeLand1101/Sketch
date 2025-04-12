#ifndef TWOSTAGE_H
#define TWOSTAGE_H

#include "Abstract.h"
#include "Util.h"

#include "CUCBF.h"
#include "CUSketch.h"
#include "MVSketch.h"
#include "CocoSketch.h"
#include "UnivMon.h"
#include "Elastic.h"
#include "ElasticHeavyPart.h"
#include "CMHeap.h"
#include "CountHeap.h"
#include "SpaceSaving.h"
#include "StableSketch.h"
#include "MomentumSketch.h"
#include "MomentumSketchSIMD.h"
#include "TightSketch.h"

#define Stage1FilterType CUSketch
#define Stage2SketchType MomentumSketch

template<typename DATA_TYPE>
class TwoStage : public Abstract<DATA_TYPE>{
public:
    typedef std::unordered_map<DATA_TYPE, COUNT_TYPE> HashMap;
    
    TwoStage(uint32_t _MEMORY, uint32_t _THRESHOLD, double _FILTER_RATIO = 0.6, double _SKETCH_RATIO = 0.4, double _ADMISSION_THRESHOLD_RATIO = 0.9){
        uint32_t FILTER_MEMORY = _MEMORY * _FILTER_RATIO;
        uint32_t SKETCH_MEMORY = _MEMORY * _SKETCH_RATIO;
        ADMISSION_TRESHOLD = _THRESHOLD * _ADMISSION_THRESHOLD_RATIO;

        filter = new Stage1FilterType<DATA_TYPE, uint16_t>(FILTER_MEMORY, 2);
        sketch = new Stage2SketchType<DATA_TYPE>(SKETCH_MEMORY, ADMISSION_TRESHOLD);

        this->name = "TwoStage ( " + filter->name + " + " + sketch->name + " )";
    }

    ~TwoStage(){
        delete filter;
        delete sketch;
    }

    void Insert(const DATA_TYPE& item){
        if (filter->Insert(item) >= ADMISSION_TRESHOLD) {
            sketch->Insert(item);
        }
    }

    COUNT_TYPE Query(const DATA_TYPE& item){
        COUNT_TYPE temp = filter->Query(item);
        if (temp >= ADMISSION_TRESHOLD) {
            return temp + sketch->Query(item);
        }
        return temp;
    }

    HashMap AllQuery(){
        return sketch->AllQuery();
    }
    
private:
    COUNT_TYPE ADMISSION_TRESHOLD;

    Stage1FilterType<DATA_TYPE, uint16_t>* filter;
    Stage2SketchType<DATA_TYPE>* sketch;
};

#endif