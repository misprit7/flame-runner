#!/usr/bin/sh

# This is a big security risk, you should be wary upon seeing this!
# It is necessary though, since memwatch has to be able to access
# dolphin RAM.
# If you're not comfortable with this you can directly use
# sudo setcap cap_sys_ptrace=eip PROGRAM_NAME
# This is very tedious when recompiling and moving things around though
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope > /dev/null
