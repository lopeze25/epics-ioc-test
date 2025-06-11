



#pragma once

#include <asynPortDriver.h>

/* This class implements an EPICS asynPortDriver for Scienta using the Mark Rivers testAsynPortDriver style */
class testAsynDriver : public asynPortDriver {
public:
    testAsynDriver(const char* portName);

    /* Override writeInt32 to support bo/longout record callbacks */
    virtual asynStatus writeInt32(asynUser* pasynUser, epicsInt32 value);

protected:
    int P_ZeroSupplies;             
};


