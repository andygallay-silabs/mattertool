import sys
import os
import random
import time
import re
import shutil
import json
import atexit

class MatterTool:
    def __init__(self) -> None:
        json_file = open("session.json")
        session_data = json.load(json_file)
        self.MATTER_ROOT = os.environ["HOME"] + session_data["MATTER_ROOT"]
        self.CHIPTOOL_PATH = self.MATTER_ROOT + session_data["CHIPTOOL_PATH"]
        self.PINCODE = session_data["PINCODE"]
        self.DISCRIMINATOR = session_data[ "DISCRIMINATOR"]
        self.ENDPOINT = session_data["ENDPOINT"]
        self.NODE_ID = session_data["NODE_ID"]
        self.LAST_NODE_ID = session_data["LAST_NODE_ID"]
        self.THREAD_DATA_SET = session_data["THREAD_DATA_SET"]
        self.SSID = session_data["SSID"]
        self.WIFI_PW = session_data["WIFI_PW"]
        self.isNodeProvided = False
        self.cmd = ""
        self.optArgs = []

        if self.NODE_ID == 0:
            self.NODE_ID = 1 + random.randint(0, 32767) % 100000

        self.cmd_list = [
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

    def CleanVars(self) -> None:
        self.DISCRIMINATOR = 3840
        self.ENDPOINT = 1
        self.NODE_ID = 0
        self.LAST_NODE_ID = 0
        self.THREAD_DATA_SET = ""
        self.SSID = ""
        self.WIFI_PW = ""

    def print_bold(self, text: str) -> None:
        print('\033[1m' + text + '\033[0m')

    def print_green(self, text: str) -> None:
        print('\033[92m' + text + '\033[0m')

    def print_blue(self, text: str) -> None:
        print('\033[94m' + text + '\033[0m')

    def PrintVars(self) -> None:
        self.print_bold("Active Vars:")
        print("MATTER_ROOT: " + self.MATTER_ROOT)
        print("CHIPTOOL_PATH: " + self.CHIPTOOL_PATH)
        print("NODE_ID: " + str(self.NODE_ID))
        print("THREAD_DATA_SET: " + self.THREAD_DATA_SET)
        print("PINCODE: " + str(self.PINCODE))
        print("DISCRIMINATOR: " + str(self.DISCRIMINATOR))
        print("SSID" + self.SSID)
        print("LAST_NODE_ID: " + str(self.LAST_NODE_ID))

        self.print_green("You can preset them with export X=Y before running the script")

    def PrintHelp(self) -> None:
        print("This Python script centralize and simplifies the use of chip-tool and starting a clean thread network")
        print("Here is and overview of the Available cmds :\n")

        for cmd in self.cmd_list:
            print(cmd)

        print("\n")

        self.print_bold("Available options :")
        print(" -h, --help			Print this help")
        print(" -n, --nodeId DIGIT		Specify the Nodeid you are trying to reach")
        print(" -di, --discriminator DIGIT		Specify the discriminator of the device to commission")
        print(" -e, --endpoint DIGIT		Specify an endpoint to the desired the cluster")
        print(" -d, --dataset HEX_STRING       Thread Operation Dataset")
        print(" -s, --ssid STRING		WiFi AP ssid that the end devices needs to connect to")
        print(" -p, --password STRING		WiFi AP password")

        self.print_green("Those configurations are held until the device is rebooted !")
        self.PrintVars()
        self.print_green("You can also enter the full chip-tool command (without the chip-tool) e.g: Mattertool levelcontrol read current-level 106 1")

    def StartThreadNetwork(self) -> None:
        self.print_green("Starting a new thread network")
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
        self.GetThreadDataset()

    def GetThreadDataset(self) -> None:
        self.THREAD_DATA_SET = os.popen("sudo ot-ctl dataset active -x").read().split("\n")[0]
        self.print_green("New ThreadDataset: " + self.THREAD_DATA_SET)

    def PairBLEThread(self) -> None:
        if self.THREAD_DATA_SET == "0":
            self.print_blue("Provide OpenThread DataSet")
            return
        
        if self.LAST_NODE_ID == self.NODE_ID:
            self.NODE_ID = 1 + random.randint(0, 32767) % 100000
        
        self.LAST_NODE_ID = self.NODE_ID
        os.system(self.CHIPTOOL_PATH + " pairing ble-thread " + 
                str(self.NODE_ID) + " hex:" + self.THREAD_DATA_SET +
                " " + str(self.PINCODE) + " " + str(self.DISCRIMINATOR))
        self.print_blue("The Node id of the commissioned device is " + str(self.NODE_ID))

    def PairBLEWiFi(self) -> None:
        if "SSID" == "":
            self.print_blue("Provide SSID")
            return
        
        if "WIFI_PW" == "":
            self.print_blue("Provide SSID password")
            return
        
        if self.LAST_NODE_ID == self.NODE_ID and self.isNodeProvided:
            self.NODE_ID = 1 + random.randint(0, 32767) % 100000

        self.print_green("Set Node id for the commissioned device : " + str(self.NODE_ID))
        self.LAST_NODE_ID = self.NODE_ID
        os.system(self.CHIPTOOL_PATH + " pairing ble-wifi " + str(self.NODE_ID)
                + " " + self.SSID + " " + self.WIFI_PW
                + " " + str(self.PINCODE) + " " + str(self.DISCRIMINATOR))
        
    def SendOnOffCmds(self) -> None:
        os.system(self.CHIPTOOL_PATH + " onoff " + self.cmd + " " + str(self.NODE_ID)
                + " " + str(self.ENDPOINT))
        
    def SendParseSetupPayload(self) -> None:
        os.system(self.CHIPTOOL_PATH + " payload parse-setup-payload " + ' '.join(self.optArgs))

    def CleanBuildChipTool(self) -> None:
        self.print_blue("Clean Build of Chip-tool")
        os.system("rm -rf " + self.MATTER_ROOT + "/out")

        for directory in os.listdir(self.MATTER_ROOT + "/tmp/"):
            if re.fullmatch("chp_.*", directory):
                shutil.rmtree(directory)

        os.system(self.MATTER_ROOT + "/scripts/examples/gn_build_example.sh " + self.MATTER_ROOT + "/examples/chip-tool " + self.MATTER_ROOT
                + "/out/standalone")
    
    def RebuildChipTool(self) -> None:
        self.print_blue("Rebuild Chip-tool")
        os.system(self.MATTER_ROOT + "/scripts/examples/gn_build_example.sh " + self.MATTER_ROOT + "/examples/chip-tool " + self.MATTER_ROOT
                + "/out/standalone")

    