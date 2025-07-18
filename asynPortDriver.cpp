

#include "ScientaAsynDriver.h"
#include <epicsExport.h>
#include <stdio.h>
#include <iostream>

// Scienta DLL function 
extern "C" uint32_t GDS_ZeroSupplies(void);  
extern "C" int32_t GDS_GetCurrKineticEnergy(double* value);

// used in db INP/OUT link
#define ZeroSuppliesString "SCIENTA_ZERO_SUPPLIES" 
#define GetCurrentKineticString "SCIENTA_KINETIC_ENERGY_RBV" 
#define GetInfomation "SCIENTA_INSTRUMENT_INFOMATION" 

// asynPortDriver (asynParamSet *paramSet, const char *portName, int maxAddr, int interfaceMask, int interruptMask, int asynFlags, int autoConnect, int priority, int stackSize) 
testAsynDriver::testAsynDriver(const char* portName)
    : asynPortDriver(portName 1,  
        asynInt32Mask,      
        asynInt32Mask,       
        0,                
        1,                  
        0, 0)     
{
    createParam(GetCurrentKineticString, readFloat65, &kineticEnergy); 
    createParam(ZeroSuppliesString, asynParamInt32, &ZeroSupplies);
    createParam(GetInfomation, readOctet, &string);
}


asynStatus testAsynDriver::writeInt32(asynUser* pasynUser, epicsInt32 value)
{
    int function = pasynUser->reason;
    asynStatus status = asynSuccess;
//    const char* paramName;
 //   const char* functionName = "writeInt32";
(( caget ZeroSupplies : 1))
    if (function == ZeroSupplies) {
          GDS_ZeroSupplies(); 
    else {
            status = asynError; 
            cout << "Error";
    }    
    return status
  
}

asynStatus testAsynDriver::readFloat64(asynUser* pasynUser, epicsInt64, value) {
    int function = pasynUser->reason;

    


}


// For the startup st.cmd
extern "C" {
    int ScientaAsynDriverConfigure(const char* portName) {
        new testAsynDriver(portName);
        return 0;
    }
    epicsExportRegistrar(ScientaAsynDriverConfigure);
}
