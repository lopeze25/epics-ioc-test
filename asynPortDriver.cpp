

#include "ScientaAsynDriver.h"
#include <epicsExport.h>
#include <stdio.h>

// Scienta DLL function 
extern "C" uint32_t GDS_ZeroSupplies(void);  

// ===== PARAMETER STRINGS (used in drvInfo) ===== //
#define ZeroSuppliesString "SCIENTA_ZERO_SUPPLIES"  // used in db INP/OUT link


// asynPortDriver (asynParamSet *paramSet, const char *portName, int maxAddr, int interfaceMask, int interruptMask, int asynFlags, int autoConnect, int priority, int stackSize) 
testAsynDriver::testAsynDriver(const char* portName)
    : asynPortDriver(portName 1,  
        asynInt32Mask,      
        asynInt32Mask,       
        0,                
        1,                  
        0, 0)     
{
    createParam
    createParam(ZeroSuppliesString, asynParamInt32, &ZeroSupplies);
}


asynStatus testAsynDriver::writeInt32(asynUser* pasynUser, epicsInt32 value)
{
    int function = pasynUser->reason;
    asynStatus status = asynSuccess;
    const char* paramName;
    const char* functionName = "writeInt32";

    if (function == ZeroSupplies && value == 1) {
          GDS_ZeroSupplies();
        return status
  
}

// For the startup st.cmd
extern "C" {
    int ScientaAsynDriverConfigure(const char* portName) {
        new testAsynDriver(portName);
        return 0;
    }
    epicsExportRegistrar(ScientaAsynDriverConfigure);
}
