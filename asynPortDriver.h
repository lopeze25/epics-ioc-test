#pragma once

#include <asynPortDriver.h>
#include <stdint.h>

class ScientaDriver : public asynPortDriver {
public:
    ScientaDriver(const char* portName);
    virtual asynStatus writeInt32(asynUser* pasynUser, epicsInt32 value) override;
    virtual asynStatus writeFloat64(asynUser* pasynUser, epicsFloat64 value) override;
    virtual asynStatus readFloat64(asynUser* pasynUser, epicsFloat64* value) override;
    virtual asynStatus readOctet(asynUser* pasynUser, char* value, size_t maxChars,
                                 size_t* nActual, int* eomReason) override;
protected:
    int P_KineticEnergy;
    int P_PassEnergy;
    int P_LensMode;
    int P_ElementSet;
    int P_ElementVoltage;
    int P_CommStatus;
    int P_ResetInstrument;
    int P_LoadInstrumentFile;
    int P_LoadRunVarFile;
    int P_ElementSetList;
    int P_LensModeList;
    int P_PassEnergyList;
