



#pragma once

#include <asynPortDriver.h>

//Based on Mark Rivers testAsynPortDriver style
class testAsynDriver : public asynPortDriver {
public:
    testAsynDriver(const char* portName);
    virtual asynStatus writeInt32(asynUser* pasynUser, epicsInt32 value);

protected:
    int ZeroSupplies;             
};


