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

def print_bold(text: str):
    print('\033[1m' + text + '\033[0m')

def print_green(text: str):
    print('\033[92m' + text + '\033[0m')

def Print_Help():
    print("This bash script centralize and simplifies the use of chip-tool and starting a clean thread network")
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
    # TODO
    None

def Clean_Vars():
    # TODO
    None

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

Print_Help()