



#pragma once

#include <asynPortDriver.h>

//Based on Mark Rivers testAsynPortDriver style
class testAsynDriver : public asynPortDriver {
public:
    testAsynDriver(const char* portName);
    virtual asynStatus writeInt32(asynUser* pasynUser, epicsInt32 value);
    virtual asynStatus readFloat64(asynUser* pasynUser, readFloat64 value); 

protected:
    int ZeroSupplies;
    int kineticEnergy; 
};


