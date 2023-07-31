
from pad import Pad, Stick, Trigger, Button
import time

with Pad('/home/xander/.local/share/dolphin-emu/Pipes/pipe1') as pad:
    pad.press_button(Button.A)
    time.sleep(1)
    pad.release_button(Button.A)
