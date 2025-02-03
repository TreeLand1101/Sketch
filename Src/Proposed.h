#ifndef PROPOSED_H
#define PROPOSED_H

#include "Abstract.h"
#include "Util.h"

#include "ColdFilter.h"
#include "MVSketch.h"

#include "CocoSketch.h"
#include "UnivMon.h"
#include "Elastic.h"
#include "CMHeap.h"
#include "CountHeap.h"
#include "SpaceSaving.h"
#include "StableSketch.h"

template<typename DATA_TYPE>
class Proposed : public Abstract<DATA_TYPE>{
public:
    typedef std::unordered_map<DATA_TYPE, COUNT_TYPE> HashMap;
    
    Proposed(uint32_t _MEMORY, uint32_t _THRESHOLD, std::string _name = "Proposed (ColdFilter + StableSketch)"){
        this->name = _name;
        uint32_t FILTER_MEMORY = _MEMORY * FILTER_RATIO;
        uint32_t SKETCH_MEMORY = _MEMORY * SKETCH_RATIO;
        threshold = _THRESHOLD;
        filter = new ColdFilter<DATA_TYPE, COUNT_TYPE>(FILTER_MEMORY, _THRESHOLD);
        sketch = new StableSketch<DATA_TYPE>(SKETCH_MEMORY, _THRESHOLD);
    }

    ~Proposed(){
        delete filter;
        delete sketch;
    }

    void Insert(const DATA_TYPE& item){
        if (filter->Insert(item) >= threshold) {
            sketch->Insert(item);
        }
    }

    COUNT_TYPE Query(const DATA_TYPE& item){
        COUNT_TYPE temp = filter->Query(item);
        if (temp >= threshold) {
            return temp + sketch->Query(item);
        }
        return temp;
    }

    HashMap AllQuery(){
        return sketch->AllQuery();
    }
    
private:
    COUNT_TYPE threshold;

    const double FILTER_RATIO = 0.5;
    const double SKETCH_RATIO = 0.5;

    const double L1_RATIO = 0.5;
    const double L2_RATIO = 0.5;

    ColdFilter<DATA_TYPE, COUNT_TYPE>* filter;
    StableSketch<DATA_TYPE>* sketch;
};

#endif