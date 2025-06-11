TOP = ../..
include $(TOP)/configure/CONFIG

PROD_IOC = myApp

myApp_SRCS += myAppMain.cpp
myApp_SRCS += testDriver.cpp

myApp_LIBS += asyn
myApp_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
