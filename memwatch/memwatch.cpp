#include "Common/CommonUtils.h"
#include "DolphinProcess/DolphinAccessor.h"

/******************************************************************************
 * Public API
 ******************************************************************************/

extern "C" {
    void init();
    uint32_t read_uint(uint32_t addr);
    float read_float(uint32_t addr);
}

void init() {
    DolphinComm::DolphinAccessor::hook();
}

uint32_t read_uint(uint32_t addr) {
    // Initialize to a recognizable value so it fails noticeably
    // Could use the return value as a success/fail indicator, but then I'd have to use a pointer
    // to return and I'm way too lazy to figure out how ctypes handles that
    int ret = 17;
    DolphinComm::DolphinAccessor::readFromRAM(
        Common::dolphinAddrToOffset(addr, DolphinComm::DolphinAccessor::isARAMAccessible()),
        (char*)&ret,
        sizeof(u32),
        true
    );
    return ret;
}

float read_float(uint32_t addr) {
    float ret = 17;
    DolphinComm::DolphinAccessor::readFromRAM(
        Common::dolphinAddrToOffset(addr, DolphinComm::DolphinAccessor::isARAMAccessible()),
        (char*)&ret,
        sizeof(u32),
        true
    );
    return ret;
}

