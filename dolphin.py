#!/usr/bin/env python

from controls.pad import Button, Pad, Stick, Trigger
import cv2, pathlib, os, time, argparse, subprocess, atexit, ctypes

from ray.rllib.env.policy_client import PolicyClient

###############################################################################
# Constants
###############################################################################

save_file = pathlib.Path().absolute() / 'luigi-circuit.sav'
dolphin_path = '/mnt/d/dolphin/'
game_file = dolphin_path + 'Games/Mario Kart Wii (USA) (En,Fr,Es).iso'
dolphin_user_path = dolphin_path + 'users/flame-runner/'
dump_url = 'rtsp://localhost:8554/dolphin'
memwatch_path = pathlib.Path().absolute() / 'memwatch/build/libmemwatch.so'

# Load memwatch dynamic library
memwatch = ctypes.CDLL(str(memwatch_path))
memwatch.read_uint.restype = ctypes.c_uint32
memwatch.read_float.restype = ctypes.c_float

###############################################################################
# Argument parse
###############################################################################

parser = argparse.ArgumentParser()
parser.add_argument(
    "--no-train", action="store_true", help="Whether to disable training."
)
parser.add_argument(
    "--inference-mode", type=str, default="local", choices=["local", "remote"]
)
parser.add_argument(
    "--stop-reward",
    type=float,
    default=9999,
    help="Stop once the specified reward is reached.",
)
parser.add_argument(
    "--port", type=int, default=9900, help="The port to use (on localhost)."
)
parser.add_argument(
    "--gui", action=argparse.BooleanOptionalAction, help="Whether to show ui of in game video"
)

args = parser.parse_args()

###############################################################################
# Setup up dolphin/mediamtx/ray
###############################################################################

processes = []
# Ask politely to terminate, might not work if process is hanging
atexit.register(lambda: [x.terminate() for x in processes])

dolphin_cmd = f'dolphin-emu-nogui --platform={"x11" if args.gui else "headless"} --exec="{game_file}" --save_state="{save_file}" --user={dolphin_user_path}'
mediamtx_cmd = 'mediamtx ./rtsp-config.yml'

print(f'Starting mediamtx server: {mediamtx_cmd}')
rtsp_process = subprocess.Popen(mediamtx_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
processes.append(rtsp_process)
time.sleep(0.3)
assert rtsp_process.poll() is None

print(f'Starting dolphin: {dolphin_cmd}')
dolphin_process = subprocess.Popen(dolphin_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
processes.append(dolphin_process)
time.sleep(3)
assert rtsp_process.poll() is None

client = PolicyClient(
    f"http://localhost:{args.port}", inference_mode=args.inference_mode
)

eid = client.start_episode(training_enabled=not args.no_train)

###############################################################################
# Connect to Dolphin
###############################################################################

print('Opening video stream')
vidcap = cv2.VideoCapture(dump_url)
memwatch.init()

###############################################################################
# Execute main training
###############################################################################

with Pad(dolphin_user_path + 'Pipes/pipe1') as pad:
    rewards = 0.0
    frame = 0
    last_time = time.time()
    pad.press_button(Button.A)
    time.sleep(0.02)
    # pad.release_button(Button.A)
    while True:
        frame += 1
        ret, image = vidcap.read()
        if not ret:
            print('RTSP read failed, aborting...')
            break

        # fps estimate
        # print(1/(time.time()-last_time))
        # last_time = time.time()
        
        if frame%10 == 0:
            action = client.get_action(eid, image)

        addr = memwatch.read_uint(0x809b8f70)
        addr = memwatch.read_uint(addr + 0xc)
        addr = memwatch.read_uint(addr)
        reward = memwatch.read_float(addr + 0xc)

        client.log_returns(eid, reward, {})

        cv2.imshow('image',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

###############################################################################
# Cleanup
###############################################################################
client.end_episode(eid, None)


