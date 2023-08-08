#include "Common/CommonUtils.h"
#include "DolphinProcess/DolphinAccessor.h"
#include <stdio.h>


int main(void){
    DolphinComm::DolphinAccessor::hook();

    char read[sizeof(u32)] = {17, 17, 17, 17};
    bool ret = DolphinComm::DolphinAccessor::readFromRAM(Common::dolphinAddrToOffset(0x80000000, DolphinComm::DolphinAccessor::isARAMAccessible()), read, sizeof(u32), false);
    printf("%d, %d, %d\n", DolphinComm::DolphinAccessor::getStatus(), read[0], ret);
}

