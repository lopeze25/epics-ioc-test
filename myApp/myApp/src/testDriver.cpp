#include <asynPortDriver.h>

class testDriver : public asynPortDriver {
public:
    testDriver(const char *portName)
        : asynPortDriver(portName, 1,
            asynInt32Mask | asynDrvUserMask,
            asynInt32Mask, 0, 0, 0, 0) {
        createParam("MY_PARAM", asynParamInt32, &paramIndex_);
        setIntegerParam(paramIndex_, 100);
    }

    virtual asynStatus writeInt32(asynUser *pasynUser, epicsInt32 value) {
        setIntegerParam(paramIndex_, value);
        callParamCallbacks();
        return asynSuccess;
    }

private:
    int paramIndex_;
};

extern "C" {
int testDriverConfig(const char *portName) {
    new testDriver(portName);
    return 0;
}
epicsExportRegistrar(testDriverConfig);
}
