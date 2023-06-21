import sys
import os
import random
import time
import re
import shutil

isNodeProvided = False
cmd = ""
optArgs=[]

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
    os.environ["NODE_ID"]= str(1 + random.randint(0, 32767) % 100000)

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
    print_blue("Clean Build of Chip-tool")
    os.system("rm -rf " + os.environ["MATTER_ROOT"] + "/out")

    for directory in os.listdir(os.environ["MATTER_ROOT/tmp/"]):
        if re.fullmatch("chp_.*", directory):
            shutil.rmtree(directory)

    os.system(os.environ["MATTER_ROOT"] + "/scripts/examples/gn_build_example.sh " + os.environ["MATTER_ROOT"] + "/examples/chip-tool " + os.environ["MATTER_ROOT"]
              + "/out/standalone")
    
    
def Rebuild_ChipTool():
    print_blue("Rebuild Chip-tool")
    os.system(os.environ["MATTER_ROOT"] + "/scripts/examples/gn_build_example.sh " + os.environ["MATTER_ROOT"] + "/examples/chip-tool " + os.environ["MATTER_ROOT"]
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
    if "THREAD_DATA_SET" in os.environ:
        os.environ["THREAD_DATA_SET"] = os.popen("sudo ot-ctl dataset active -x").read().split("\n")[0]
        print_green("New ThreadDataset: " + os.environ["THREAD_DATA_SET"])

def Pair_BLE_Thread():
    if os.environ["THREAD_DATA_SET"] == "0":
        print_blue("Provide OpenThread DataSet")
        return
    
    if os.environ["LAST_NODE_ID"] == os.environ["NODE_ID"]:
        os.environ["NODE_ID"] = str(1 + random.randint(0, 32767) % 100000)
    
    os.environ["LAST_NODE_ID"] = os.environ["NODE_ID"]
    os.system(os.environ["CHIPTOOL_PATH"] + " pairing ble-thread " + 
              os.environ["NODE_ID"] + " hex:" + os.environ["THREAD_DATA_SET"] +
              " " + os.environ["PINCODE"] + " " + os.environ["DISCRIMINATOR"])
    print_blue("The Node id of the commissioned device is " + os.environ["NODE_ID"])

def Pair_BLE_WiFi():
    if "SSID" not in os.environ:
        print_blue("Provide SSID")
        return
    
    if "WIFI_PW" not in os.environ:
        print_blue("Provide SSID password")
        return
    
    if os.environ["LAST_NODE_ID"] == os.environ["NODE_ID"] and isNodeProvided:
        os.environ["NODE_ID"] = str(1 + random.randint(0, 32767) % 100000)

    print_green("Set Node id for the commissioned device : " + os.environ("NODE_ID"))
    os.environ["LAST_NODE_ID"] = os.environ["NODE_ID"]
    os.system(os.environ["CHIPTOOL_PATH"] + " pairing ble-wifi " + os.environ["NODE_ID"]
              + " " + os.environ["SSID"] + " " + os.environ["WIFI_PW"]
              + " " + os.environ["PINCODE"] + " " + os.environ["DISCRIMINATOR"])

def Send_OnOff_Cmds():
    os.system(os.environ["CHIPTOOL_PATH"] + " onoff " + cmd + " " + os.environ["NODE_ID"]
              + " " + os.environ["ENDPOINT"])

def Send_ParseSetupPayload():
    os.system(os.environ["CHIPTOOL_PATH"] + " payload parse-setup-payload " + ' '.join(optArgs))


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
if pipEnv not in os.environ["MATTER_ROOT"]:
    os.system(os.environ["MATTER_ROOT"] + "/scripts/activate.sh")

# Get arguments and remove the first one (invocation of pychip.py)
sys_argv = sys.argv
del(sys_argv[0])

# Switch case depending on the arguments, parse the arguments until no more to parse
exit = False
while not exit:
    if len(sys_argv) == 0 and cmd != "":
        if cmd in cmd_list:
            cmd_dict[cmd]()
        else:
            os.system(os.environ["CHIPTOOL_PATH"] + cmd + " " + ' '.join(optArgs))
        cmd = ""

    if len(sys_argv) == 0:
        os.system(os.environ["CHIPTOOL_PATH"])
        print("")
        print("> Press q to end pychip session or enter any argument.")
        user_inputs = input()

        if user_inputs == "q":
            exit = True
            break

        user_inputs = user_inputs.split()
        for user_input  in user_inputs:
            sys_argv.append(user_input)


    if len(sys_argv) > 0:
        if sys_argv[0] == "--help" or sys_argv[0] == "-h":
            Print_Help()
            del(sys_argv[0])
            continue

        if sys_argv[0] == "--nodeId" or sys_argv[0] == "-n":
            if len(sys_argv) < 2:
                print_blue("Provide node ID value")
                del(sys_argv[0])
            else:
                os.environ["NODE_ID"] = sys_argv[1]
                isNodeProvided = True
                del(sys_argv[0])
                del(sys_argv[0])
            continue
        
        if sys_argv[0] == "--discriminator" or sys_argv[0] == "-di":
            if len(sys_argv) < 2:
                print_blue("Provide discriminator value")
                del(sys_argv[0])
            else:
                os.environ["DISCRIMINATOR"] = sys_argv[1]
                del(sys_argv[0])
                del(sys_argv[0])
            continue

        if sys_argv[0] == "--endpoint" or sys_argv[0] == "-e":
            if len(sys_argv) < 2:
                print_blue("Provide endpoint value")
                del(sys_argv[0])
            else:
                os.environ["ENDPOINT"] = sys_argv[1]
                del(sys_argv[0])
                del(sys_argv[0])
            continue

        if sys_argv[0] == "--dataset" or sys_argv[0] == "-d":
            if len(sys_argv) < 2:
                print_blue("Provide dataset Hex value")
                del(sys_argv[0])
            else:
                os.environ["THREAD_DATA_SET"] = sys_argv[1]
                del(sys_argv[0])
                del(sys_argv[0])
            continue

        if sys_argv[0] == "--ssid" or sys_argv[0] == "-s":
            if len(sys_argv) < 2:
                print_blue("Provide SSID name")
            else:
                os.environ["SSID"] = sys_argv[1]
                del(sys_argv[0])
                del(sys_argv[0])
            continue

        if sys_argv[0] == "--password" or sys_argv[0] == "-p":
            if len(sys_argv) < 2:
                print_blue("Provide SSID password")
                del(sys_argv[0])
            else:
                os.environ["WIFI_PW"] = sys_argv[1]
                del(sys_argv[0])
                del(sys_argv[0])
            continue

    if cmd == "":
        cmd = sys_argv[0]
    else:
        optArgs.append(sys_argv[0])
    del(sys_argv[0])
