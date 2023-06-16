import sys
import os
import random

if "MATTER_ROOT" not in os.environ:
    os.environ["MATTER_ROOT"] = os.environ["HOME"] + "/connectedhomeip"

if "CHIPTOOL_PATH" not in os.environ:
    os.environ["CHIPTOOL_PATH"] = os.environ["MATTER_ROOT"] + "/out/standalone/chip-tool"

if "PINCODE" not in os.environ:
    os.environ["PINCODE"] = "20202021"

if "DISCRIMINATOR" not in os.environ:
    os.environ["DISCRIMINATOR"]="3840"

if "ENDPOINT" not in os.environ:
    os.environ["ENDPOINT"]="1"

if "NODE_ID" not in os.environ:
    os.environ["NODE_ID"]= str(1 + random.randint(0, 1000000))

if "LAST_NODE_ID" not in os.environ:
    os.environ["LAST_NODE_ID"] = "0"

if "THREAD_DATA_SET" not in os.environ:
    os.environ["THREAD_DATA_SET"] = "0"

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
    print("MATTER_ROOT: " + os.environ["MATTER_ROOT"])
    print("CHIPTOOL_PATH: " + os.environ["CHIPTOOL_PATH"])
    print("NODE_ID: " + os.environ["NODE_ID"])
    print("THREAD_DATA_SET: " + os.environ["THREAD_DATA_SET"])
    print("PINCODE: " + os.environ["PINCODE"])
    print("DISCRIMINATOR: " + os.environ["DISCRIMINATOR"])
    if "SSID" in os.environ:
        print("SSID: " + os.environ["SSID"])
    print("LAST_NODE_ID: " + os.environ["LAST_NODE_ID"])

    print_green("You can preset them with export X=Y before running the script")

def Clean_Vars():
    print_blue("Erasing Vars:")
    for env_var in env_vars_list:
        if env_var in os.environ:
            print(env_var)
            os.unsetenv(env_var)

def Clean_build_ChipTool():
    # TODO
    None

def Rebuild_ChipTool():
    # TODO
    None

def Start_ThreadNetwork():
    # TODO
    None

def Get_ThreadDataset():
    # TODO
    None

def Pair_BLE_Thread():
    # TODO
    None

def Pair_BLE_WiFi():
    # TODO
    None

def Send_OnOff_Cmds():
    # TODO
    None

def Send_ParseSetupPayload():
    # TODO
    None

def Send_ParseSetupPayload():
    # TODO
    None

if len(sys.argv) > 1:
    if sys.argv[1] == "--help":
        Print_Help()
    
    if sys.argv[1] == "--vars":
        Print_Vars()

    if sys.argv[1] == "--cleanVars":
        Clean_Vars()