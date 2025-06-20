#ifndef OTHERABSTRACT_H
#define OTHERABSTRACT_H

#include <unordered_map>

#include <string.h>

#include "Util.h"

template<typename DATA_TYPE>
class Abstract{
public:
    Abstract(){}
    virtual ~Abstract(){};

    std::string name;
    COUNT_TYPE stage1_bias;
    
    typedef std::unordered_map<DATA_TYPE, COUNT_TYPE> HashMap;

    virtual void Insert(const DATA_TYPE& item) = 0;
    virtual COUNT_TYPE Query(const DATA_TYPE& item) = 0;
    virtual HashMap AllQuery() = 0;
};

#endif
