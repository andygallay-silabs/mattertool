import sys
import os
import random
import time
import re
import shutil
import json
import atexit

isNodeProvided = False
cmd = ""
optArgs=[]

# Session loading
json_file = open("session.json")
session_data = json.load(json_file)

MATTER_ROOT = os.environ["HOME"] + session_data["MATTER_ROOT"]
CHIPTOOL_PATH = MATTER_ROOT + session_data["CHIPTOOL_PATH"]
PINCODE = session_data["PINCODE"]   
DISCRIMINATOR = session_data["DISCRIMINATOR"]
ENDPOINT = session_data["ENDPOINT"]
NODE_ID = session_data["NODE_ID"]
LAST_NODE_ID = session_data["LAST_NODE_ID"]
THREAD_DATA_SET = session_data["THREAD_DATA_SET"]
SSID = session_data["SSID"]
WIFI_PW = session_data["WIFI_PW"]

if NODE_ID == 0:
    NODE_ID = 1 + random.randint(0, 32767) % 100000

def atexit_handler():
    json_file = open("session.json", "r")
    session_data = json.load(json_file)

    session_data["NODE_ID"] = NODE_ID
    session_data["LAST_NODE_ID"] = LAST_NODE_ID
    session_data["THREAD_DATA_SET"] = THREAD_DATA_SET
    session_data["SSID"] = SSID
    session_data["WIFI_PW"] = WIFI_PW

    json_file.close()
    json_file = open("session.json", "w")

    json.dump(session_data, json_file)
    json_file.close()

atexit.register(atexit_handler)

cmd_list =[
    "help",
    "vars",
    "cleanVars",
    "buildCT",
    "rebuildCT",
    "startThread",
    "getThreadDataset",
    "bleThread",
    "bleWifi",
    "on",
    "off",
    "toggle",
    "parsePayload"        
]

env_vars_list = [
    "MATTER_ROOT",
    "CHIPTOOL_PATH",
    "NODE_ID",
    "THREAD_DATA_SET",
    "PINCODE",
    "DISCRIMINATOR",
    "SSID",
    "WIFI_PW",
    "LAST_NODE_ID"
]

def print_bold(text: str):
    print('\033[1m' + text + '\033[0m')

def print_green(text: str):
    print('\033[92m' + text + '\033[0m')

def print_blue(text: str):
    print('\033[94m' + text + '\033[0m')

def Print_Help():
    print("This Python script centralize and simplifies the use of chip-tool and starting a clean thread network")
    print("Here is and overview of the Available cmds :\n")

    for cmd in cmd_list:
        print(cmd)

    print("\n")

    print_bold("Available options :")
    print(" -h, --help			Print this help")
    print(" -n, --nodeId DIGIT		Specify the Nodeid you are trying to reach")
    print(" -di, --discriminator DIGIT		Specify the discriminator of the device to commission")
    print(" -e, --endpoint DIGIT		Specify an endpoint to the desired the cluster")
    print(" -d, --dataset HEX_STRING       Thread Operation Dataset")
    print(" -s, --ssid STRING		WiFi AP ssid that the end devices needs to connect to")
    print(" -p, --password STRING		WiFi AP password")

    print_green("Those configurations are held until the device is rebooted !")
    Print_Vars()
    print_green("You can also enter the full chip-tool command (without the chip-tool) e.g: Mattertool levelcontrol read current-level 106 1")


def Print_Vars():
    print_bold("Active Vars:")
    print("MATTER_ROOT: " + MATTER_ROOT)
    print("CHIPTOOL_PATH: " + CHIPTOOL_PATH)
    print("NODE_ID: " + str(NODE_ID))
    print("THREAD_DATA_SET: " + THREAD_DATA_SET)
    print("PINCODE: " + str(PINCODE))
    print("DISCRIMINATOR: " + str(DISCRIMINATOR))
    print("SSID" + SSID)
    print("LAST_NODE_ID: " + str(LAST_NODE_ID))

    print_green("You can preset them with export X=Y before running the script")

def Clean_Vars():
    global DISCRIMINATOR
    global ENDPOINT
    global NODE_ID
    global LAST_NODE_ID
    global THREAD_DATA_SET
    global SSID
    global WIFI_PW
    print_blue("Erasing Vars")
    DISCRIMINATOR = 3840
    ENDPOINT = 1
    NODE_ID = 0
    LAST_NODE_ID = 0
    THREAD_DATA_SET = ""
    SSID = ""
    WIFI_PW = ""

def Clean_build_ChipTool():
    print_blue("Clean Build of Chip-tool")
    os.system("rm -rf " + MATTER_ROOT + "/out")

    for directory in os.listdir(MATTER_ROOT + "/tmp/"):
        if re.fullmatch("chp_.*", directory):
            shutil.rmtree(directory)

    os.system(MATTER_ROOT + "/scripts/examples/gn_build_example.sh " + MATTER_ROOT + "/examples/chip-tool " + MATTER_ROOT
              + "/out/standalone")
    
    
def Rebuild_ChipTool():
    print_blue("Rebuild Chip-tool")
    os.system(MATTER_ROOT + "/scripts/examples/gn_build_example.sh " + MATTER_ROOT + "/examples/chip-tool " + MATTER_ROOT
              + "/out/standalone")

def Start_ThreadNetwork():
    print_green("Starting a new thread network")
    os.system("sudo ot-ctl factoryreset")
    time.sleep(3)
    os.system("sudo ot-ctl srp server disable")
    os.system("sudo ot-ctl srp server enable")
    os.system("sudo ot-ctl thread stop")
    os.system("sudo ot-ctl ifconfig down")
    os.system("sudo ot-ctl ifconfig up")
    os.system("sudo ot-ctl prefix add fd11:22::/64 paros")
    os.system("sudo ot-ctl thread start")
    time.sleep(7)
    os.system("sudo ot-ctl extpanid")
    Get_ThreadDataset()

def Get_ThreadDataset():
    THREAD_DATA_SET = os.popen("sudo ot-ctl dataset active -x").read().split("\n")[0]
    print_green("New ThreadDataset: " + THREAD_DATA_SET)

def Pair_BLE_Thread():
    if THREAD_DATA_SET == "0":
        print_blue("Provide OpenThread DataSet")
        return
    
    if LAST_NODE_ID == NODE_ID:
        NODE_ID = 1 + random.randint(0, 32767) % 100000
    
    LAST_NODE_ID = NODE_ID
    os.system(CHIPTOOL_PATH + " pairing ble-thread " + 
              str(NODE_ID) + " hex:" + THREAD_DATA_SET +
              " " + str(PINCODE) + " " + str(DISCRIMINATOR))
    print_blue("The Node id of the commissioned device is " + str(NODE_ID))

def Pair_BLE_WiFi():
    if "SSID" == "":
        print_blue("Provide SSID")
        return
    
    if "WIFI_PW" == "":
        print_blue("Provide SSID password")
        return
    
    if LAST_NODE_ID == NODE_ID and isNodeProvided:
        NODE_ID = 1 + random.randint(0, 32767) % 100000

    print_green("Set Node id for the commissioned device : " + str(NODE_ID))
    LAST_NODE_ID = NODE_ID
    os.system(CHIPTOOL_PATH + " pairing ble-wifi " + str(NODE_ID)
              + " " + SSID + " " + WIFI_PW
              + " " + str(PINCODE) + " " + str(DISCRIMINATOR))

def Send_OnOff_Cmds():
    os.system(CHIPTOOL_PATH + " onoff " + cmd + " " + str(NODE_ID)
              + " " + str(ENDPOINT))

def Send_ParseSetupPayload():
    os.system(CHIPTOOL_PATH + " payload parse-setup-payload " + ' '.join(optArgs))


cmd_dict = {
    "help": Print_Help,
    "vars": Print_Vars,
    "cleanVars": Clean_Vars,
    "buildCT": Clean_build_ChipTool,
    "rebuildCT": Rebuild_ChipTool,
    "startThread": Start_ThreadNetwork,
    "getThreadDataset": Get_ThreadDataset,
    "bleThread": Pair_BLE_Thread,
    "bleWifi": Pair_BLE_WiFi,
    "on": Send_OnOff_Cmds,
    "off": Send_OnOff_Cmds,
    "toggle": Send_OnOff_Cmds,
    "parsePayload": Send_ParseSetupPayload   
}

pipEnv = os.popen("pip -V").read()

# Activate Matter environment if it isn't already
if pipEnv not in MATTER_ROOT:
    os.system(MATTER_ROOT + "/scripts/activate.sh")

# Get arguments and remove the first one (invocation of mattertool.py)
sys_argv = sys.argv
del(sys_argv[0])

# Switch case depending on the arguments, parse the arguments until no more to parse
while len(sys_argv) >= 1:
    if sys_argv[0] == "--help" or sys_argv[0] == "-h":
        Print_Help()
        del(sys_argv[0])
        continue

    if sys_argv[0] == "--nodeId" or sys_argv[0] == "-n":
        if len(sys_argv) < 2:
            print_blue("Provide node ID value")
            del(sys_argv[0])
        else:
            NODE_ID = int(sys_argv[1])
            isNodeProvided = True
            del(sys_argv[0])
            del(sys_argv[0])
        continue
    
    if sys_argv[0] == "--discriminator" or sys_argv[0] == "-di":
        if len(sys_argv) < 2:
            print_blue("Provide discriminator value")
            del(sys_argv[0])
        else:
            DISCRIMINATOR = int(sys_argv[1])
            del(sys_argv[0])
            del(sys_argv[0])
        continue

    if sys_argv[0] == "--endpoint" or sys_argv[0] == "-e":
        if len(sys_argv) < 2:
            print_blue("Provide endpoint value")
            del(sys_argv[0])
        else:
            ENDPOINT = int(sys_argv[1])
            del(sys_argv[0])
            del(sys_argv[0])
        continue

    if sys_argv[0] == "--dataset" or sys_argv[0] == "-d":
        if len(sys_argv) < 2:
            print_blue("Provide dataset Hex value")
            del(sys_argv[0])
        else:
            THREAD_DATA_SET = sys_argv[1]
            del(sys_argv[0])
            del(sys_argv[0])
        continue

    if sys_argv[0] == "--ssid" or sys_argv[0] == "-s":
        if len(sys_argv) < 2:
            print_blue("Provide SSID name")
        else:
            SSID = sys_argv[1]
            del(sys_argv[0])
            del(sys_argv[0])
        continue

    if sys_argv[0] == "--password" or sys_argv[0] == "-p":
        if len(sys_argv) < 2:
            print_blue("Provide SSID password")
            del(sys_argv[0])
        else:
            WIFI_PW = sys_argv[1]
            del(sys_argv[0])
            del(sys_argv[0])
        continue

    if cmd == "":
        cmd = sys_argv[0]
    else:
        optArgs.append(sys_argv[0])
    del(sys_argv[0])

if cmd in cmd_list:
    cmd_dict[cmd]()
else:
    os.system(CHIPTOOL_PATH + cmd + " " + ' '.join(optArgs))