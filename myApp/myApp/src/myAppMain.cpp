#include <iocsh.h>
#include "epicsExit.h"
#include "epicsThread.h"

int main(int argc, char *argv[]) {
    if (argc >= 2) {
        iocsh(argv[1]);
    } else {
        iocsh(NULL);
    }
    epicsExit(0);
    return 0;
}
