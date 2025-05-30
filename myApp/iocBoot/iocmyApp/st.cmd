cd ../../

dbLoadDatabase("dbd/myApp.dbd")
testDriverConfig("TEST_PORT")
dbLoadRecords("db/myApp.db")
iocInit()
