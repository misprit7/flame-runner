# Gecko Scripts

## Checkpoints:
Taken from [here](https://mariokartwii.com/showthread.php?tid=1017).
```
#Address ports
#80530930 = NTSC-U
#80535478 = PAL
#80534DF8 = NTSC-J
#805234D0 = NTSC-K

.set region, '' #Must set region value, or else source will not compile

.if (region == 'E' || region == 'e') # RMCE
    .set _1sthalf, 0x8053
    .set _2ndhalf, 0x10A0
.elseif (region == 'P' || region == 'p') # RMCP
    .set _1sthalf, 0x8053
    .set _2ndhalf, 0x5BE8
.elseif (region == 'J' || region == 'j') # RMCJ
    .set _1sthalf, 0x8053
    .set _2ndhalf, 0x5568
.elseif (region == 'K' || region == 'k') # RMCK
    .set _1sthalf, 0x8052
    .set _2ndhalf, 0x3C40
.else # Invalid Region
    .err
.endif

#Default Instruction, r6 holds checkpoint region value
lhz r6, 0x000A (r30)

#Set Address upper bits, Or in ckpt value
lis r12, _1sthalf
oris r11, r6, 0x38A0 #Or 0x38A00000 to r6

#Write new instruction in memory, store data cache, invalidate instruction cache
stwu r11, 0 (r12) # NOTE: Added manually, writes to arbitrary memory address
stwu r11, _2ndhalf (r12)
dcbst 0, r12
sync
icbi 0, r12
isync
```

## Speedometer
Taken from [here](https://mariokartwii.com/showthread.php?tid=1730).

