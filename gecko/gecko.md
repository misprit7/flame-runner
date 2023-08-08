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
```
# inject at 80857ca0 (PAL)
# inject at 80836210 (NTSC-U)
# inject at 8085730c (NTSC-J)
# inject at 80846060 (NTSC-K)

add r3, r3, r30 # increase the control count by one speedometer per local player

lwz r31, 0x1c (r1) # original instruction
```

```
# replace at 80857edc (PAL)
# replace at 8083644c (NTSC-U)
# replace at 80857548 (NTSC-J)
# replace at 8084629c (NTSC-K)

# always create (at least) one CtrlRaceBattlePoint per player
# also reset the lsb which is used to know if the control is regular
rlwinm r21, r21, 0, 24, 24
```

```
# inject at 805e88f0 (PAL)
# inject at 805d2204 (NTSC-U)
# inject at 805e81cc (NTSC-J)
# inject at 805d6a8c (NTSC-K)

.set coin, 0x636f696e

bctrl # original instruction

lwz r4, 0x0 (r19) # get the brlyt name
lis r5, coin@h
ori r5, r5, coin@l
cmpw r4, r5 # check if it starts with "coin"
bne end # if not, we are done

# otherwise, patch the brlyt

# change the text pane size
lis r4, 0x4370 # 240.0f
stw r4, 0x190 (r3)

# change the maximum string size of the text pane
li r4, 0x20
sth r4, 0x198 (r3)

end:
```

```
# inject at 805e88f0 (PAL)
# inject at 805d2204 (NTSC-U)
# inject at 805e81cc (NTSC-J)
# inject at 805d6a8c (NTSC-K)

.set coin, 0x636f696e

bctrl # original instruction

lwz r4, 0x0 (r19) # get the brlyt name
lis r5, coin@h
ori r5, r5, coin@l
cmpw r4, r5 # check if it starts with "coin"
bne end # if not, we are done

# otherwise, patch the brlyt

# change the text pane size
lis r4, 0x4370 # 240.0f
stw r4, 0x190 (r3)

# change the maximum string size of the text pane
li r4, 0x20
sth r4, 0x198 (r3)

end:
Code:
# inject at 80857f4c (PAL)
# inject at 808364bc (NTSC-U)
# inject at 808575b8 (NTSC-J)
# inject at 8084630c (NTSC-K)

.set region, ''

.if (region == 'P')
    .set SystemManager_s_instance, 0x80386000
.elseif (region == 'E')
    .set SystemManager_s_instance, 0x80381c80
.elseif (region == 'J')
    .set SystemManager_s_instance, 0x80385980
.elseif (region == 'K')
    .set SystemManager_s_instance, 0x80374020
.else
    .err
.endif

andi. r0, r21, 0x1 # check if we are creating a custom control
bne end # if not, we are (almost) done

mflr r5 # backup the lr

bl positions
# 4:3 x
.short 0x4358 # 1/1: 216.0f
.short 0xc30c # 1/2: -140.0f
.short 0xc30c # 2/2: -140.0f
.short 0xc365 # 1/4: -229.0f
.short 0x436c # 2/4: 236.0f
.short 0xc365 # 3/4: -229.0f
.short 0x436c # 4/4: 236.0f

# 4:3 y
.short 0xc336 # 1/1: -182.0f
.short 0x41d0 # 1/2: 26.0f
.short 0xc343 # 2/2: -195.0f
.short 0x42dc # 1/4: 110.0f
.short 0x42dc # 2/4: 110.0f
.short 0xc2d2 # 3/4: -105.0f
.short 0xc2d2 # 4/4: -105.0f

# 16:9 x
.short 0x4398 # 1/1: 304.0f
.short 0xc366 # 1/2: -230.0f
.short 0xc366 # 2/2: -230.0f
.short 0xc3a6 # 1/4: -332.0f
.short 0x43ac # 2/4: 344.0f
.short 0xc3a6 # 3/4: -332.0f
.short 0x43ac # 4/4: 344.0f

# 16:9 y
.short 0xc33e # 1/1: -190.0f
.short 0x41c8 # 1/2: 25.0f
.short 0xc347 # 2/2: -199.0f
.short 0x42e6 # 1/4: 115.0f
.short 0x42e6 # 2/4: 115.0f
.short 0xc2e6 # 3/4: -115.0f
.short 0xc2e6 # 4/4: -115.0f
positions:
mflr r3

# compute the address
lbz r4, 0x8 + 0xe (r1)
subi r4, r4, 0x30 + 0x1
add r4, r4, r17
slwi r4, r4, 1
add r3, r3, r4
lis r4, SystemManager_s_instance@ha
lwz r4, SystemManager_s_instance@l (r4)
lwz r4, 0x58 (r4)
mulli r4, r4, 0x1c
add r3, r3, r4

# set the x position
lhz r4, 0x0 (r3)
sth r4, 0x1c (r20)

# set the y position
lhz r4, 0xe (r3)
sth r4, 0x20 (r20)

# access the layout
lwz r3, 0xbc (r20)
lwz r3, 0x14 (r3)
lwz r3, -0x4 + 0x14 (r3)

# set the scale
lis r4, 0x3e80
stw r4, -0x4 + 0x44 (r3)
stw r4, -0x4 + 0x48 (r3)

# align the text to the right
li r4, 0x2
stb r4, -0x4 + 0x100 (r3)

addi r3, r5, 0x6c # setup the lr to skip the creation of the CtrlRaceBattleAddPoint

cmpwi r21, 0x0 # check if the battle point controls are disabled
beq jump

subi r3, r5, 0x6c # setup the lr to create the second CtrlRaceBattlePoint
ori r21, r21, 0x1 # mark the custom control as created

jump:
mtlr r3
blr

end:
stb r0, 0x81 (r20) # mark the control as regular

li r3, 0x208 # original instruction
```

```
# inject at 805f8c88 (PAL)
# inject at 805d83a4 (NTSC-U)
# inject at 805f8564 (NTSC-J)
# inject at 805e70a8 (NTSC-K)

cmpwi r4, 0x0 # check if the message id is a pointer
bge end # is not, we are done

# otherwise return it as a slot
mr r3, r4
blr

end:
lwz r5, 0x10 (r3) # original instruction
```

```
# replace at 805f8d08 (PAL)
# replace at 805d8424 (NTSC-U)
# replace at 805f85e4 (NTSC-J)
# replace at 805e7128 (NTSC-K)

mr r3, r4 # if the slot is a pointer, return it as the message
```

```
# replace at 805f8d44 (PAL)
# replace at 805d8460 (NTSC-U)
# replace at 805f8620 (NTSC-J)
# replace at 805e7164 (NTSC-K)

.set region, ''

.if (region == 'P')
    .set offset, 0x403c
.elseif (region == 'E')
    .set offset, 0x403c
.elseif (region == 'J')
    .set offset, 0x403c
.elseif (region == 'K')
    .set offset, 0x401c
.else
    .err
.endif

# if the slot is a pointer, return a pointer to the attributes
# we have the wanted value somewhere in sdata2
subi r3, r13, offset
```

```
# replace at 805cddac (PAL)
# replace at 805c128c (NTSC-U)
# replace at 805cd688 (NTSC-J)
# replace at 805bbd6c (NTSC-K)

# only consider -1 as "no slot found"
cmpwi r20, -0x1
bne 0xc
```

