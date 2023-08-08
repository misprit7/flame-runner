cmake_minimum_required(VERSION 3.5.0)
project(memwatch)

set(DolphinProcessSrc DolphinProcess/Linux/LinuxDolphinProcess.cpp)

set(SRCS ${DolphinProcessSrc}
         DolphinProcess/DolphinAccessor.cpp  
         Common/MemoryCommon.cpp)

set(CMAKE_INCLUE_CURRENT_DIR ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# add_executable(memwatch ${SRCS} main.cpp)
add_library(memwatch SHARED ${SRCS} memwatch.cpp)

