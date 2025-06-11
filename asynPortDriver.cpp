

#include "ScientaAsynDriver.h"
#include <epicsExport.h>
#include <stdio.h>


extern "C" uint32_t GDS_ZeroSupplies(void);  // Scienta DLL function

// ===== PARAMETER STRINGS (used in drvInfo) ===== //
#define P_ZeroSuppliesString "SCIENTA_ZERO_SUPPLIES"  // used in db INP/OUT link

// ===== Constructor ===== //
ScientaAsynDriver::ScientaAsynDriver(const char* portName)
    : asynPortDriver(portName 1,  // maxAddr
        asynInt32Mask,       // Interface mask
        asynInt32Mask,       // Interrupt mask
        0,                   // asynFlags (non-blocking, single device)
        1,                   // autoConnect
        0, 0)                // priority, stack size
{
    // ===== Create Parameters ===== //
    createParam(P_ZeroSuppliesString, asynParamInt32, &P_ZeroSupplies);
}


asynStatus testAsynDriver::writeInt32(asynUser* pasynUser, epicsInt32 value)
{
    int function = pasynUser->reason;
    asynStatus status = asynSuccess;
    const char* paramName;
    const char* functionName = "writeInt32";


    if (function == P_ZeroSupplies && value == 1) {
        uint32_t err = GDS_ZeroSupplies();
        if (err > 0) {
            printf("%s::%s: GDS_ZeroSupplies failed with code %u\n", driverName, functionName, err);
            status = asynError;
        }
        else {
            printf("%s::%s: Successfully zeroed Scienta voltages.\n", driverName, functionName);
        }
    }

    // Notify any connected clients (e.g., EPICS records)
    callParamCallbacks();

}
// ===== EPICS Registration ===== //
extern "C" {
    int ScientaAsynDriverConfigure(const char* portName) {
        new testAsynDriver(portName);
        return 0;
    }
    epicsExportRegistrar(ScientaAsynDriverConfigure);
}
