import sys
import os
import json
import atexit
import subprocess

import mattertool

matterTool = mattertool.MatterTool()

def atexit_handler():
    json_file = open("./session.json", "r")
    session_data = json.load(json_file)

    session_data["NODE_ID"] = matterTool.NODE_ID
    session_data["LAST_NODE_ID"] = matterTool.LAST_NODE_ID
    session_data["THREAD_DATA_SET"] = matterTool.THREAD_DATA_SET
    session_data["SSID"] = matterTool.SSID
    session_data["WIFI_PW"] = matterTool.WIFI_PW
    session_data["VERBOSE"] = matterTool.VERBOSE

    json_file.close()
    json_file = open("session.json", "w")

    json.dump(session_data, json_file)
    json_file.close()

# Function run on program termination
atexit.register(atexit_handler)

cmd_dict = {
    "help": matterTool.PrintHelp,
    "vars": matterTool.PrintVars,
    "cleanVars": matterTool.CleanVars,
    "buildCT": matterTool.CleanBuildChipTool,
    "rebuildCT": matterTool.RebuildChipTool,
    "startThread": matterTool.StartThreadNetwork,
    "getThreadDataset": matterTool.GetThreadDataset,
    "bleThread": matterTool.PairBLEThread,
    "bleWifi": matterTool.PairBLEWiFi,
    "on": matterTool.SendOnOffCmds,
    "off": matterTool.SendOnOffCmds,
    "toggle": matterTool.SendOnOffCmds,
    "parsePayload": matterTool.SendParseSetupPayload,
    "toggleVerbose": matterTool.ToggleVerbose   
}

pipEnv = os.popen("pip -V").read()

# Activate Matter environment if it isn't already
if pipEnv not in matterTool.MATTER_ROOT:
    subprocess.run([matterTool.MATTER_ROOT + "/scripts/activate.sh"], shell=True, capture_output=True)

# Get arguments and remove the first one (invocation of mattertool.py)
sys_argv = sys.argv
del(sys_argv[0])

# Switch case depending on the arguments, parse the arguments until no more to parse
while len(sys_argv) >= 1:
    if sys_argv[0] == "--help" or sys_argv[0] == "-h":
        matterTool.PrintHelp()
        del(sys_argv[0])
        continue

    if sys_argv[0] == "--nodeId" or sys_argv[0] == "-n":
        if len(sys_argv) < 2:
            matterTool.print_blue("Provide node ID value")
            del(sys_argv[0])
        else:
            matterTool.NODE_ID = int(sys_argv[1])
            matterTool.isNodeProvided = True
            del(sys_argv[0])
            del(sys_argv[0])
        continue
    
    if sys_argv[0] == "--discriminator" or sys_argv[0] == "-di":
        if len(sys_argv) < 2:
            matterTool.print_blue("Provide discriminator value")
            del(sys_argv[0])
        else:
            matterTool.DISCRIMINATOR = int(sys_argv[1])
            del(sys_argv[0])
            del(sys_argv[0])
        continue

    if sys_argv[0] == "--endpoint" or sys_argv[0] == "-e":
        if len(sys_argv) < 2:
            matterTool.print_blue("Provide endpoint value")
            del(sys_argv[0])
        else:
            matterTool.ENDPOINT = int(sys_argv[1])
            del(sys_argv[0])
            del(sys_argv[0])
        continue

    if sys_argv[0] == "--dataset" or sys_argv[0] == "-d":
        if len(sys_argv) < 2:
            matterTool.print_blue("Provide dataset Hex value")
            del(sys_argv[0])
        else:
            matterTool.THREAD_DATA_SET = sys_argv[1]
            del(sys_argv[0])
            del(sys_argv[0])
        continue

    if sys_argv[0] == "--ssid" or sys_argv[0] == "-s":
        if len(sys_argv) < 2:
            matterTool.print_blue("Provide SSID name")
        else:
            matterTool.SSID = sys_argv[1]
            del(sys_argv[0])
            del(sys_argv[0])
        continue

    if sys_argv[0] == "--password" or sys_argv[0] == "-p":
        if len(sys_argv) < 2:
            matterTool.print_blue("Provide SSID password")
            del(sys_argv[0])
        else:
            matterTool.WIFI_PW = sys_argv[1]
            del(sys_argv[0])
            del(sys_argv[0])
        continue

    if matterTool.cmd == "":
        matterTool.cmd = sys_argv[0]
    else:
        matterTool.optArgs.append(sys_argv[0])
    del(sys_argv[0])

if matterTool.cmd in matterTool.cmd_list:
    cmd_dict[matterTool.cmd]()
else:
    run_args = [matterTool.CHIPTOOL_PATH, matterTool.cmd] + matterTool.optArgs
    subprocess.run(run_args, shell=True)