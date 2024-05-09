import asyncio, pyvts
from random import randint
from time import sleep
from colors import *
import os

plugin_info = {
    "plugin_name": "start pyvts",
    "developer": "Kepha Sher",
    "authentication_token_path": os.path.dirname(__file__) + '/token.txt'
}

# the hotkeys are custom, configure it in VTS
MAP = {'happy': 'motion4', 'neutral': 'motion1', 'suprised': 'motion5',  'fear': 'motion6', 'anger': 'motion7'}

async def main():
    vts = pyvts.vts(plugin_info=plugin_info)
    await vts.connect()
    await vts.request_authenticate_token()  # get token and wait
    await vts.request_authenticate()
    x = 0
    while True:
        action = open("action.txt", "r").readline().strip()
        if len(action) > 0:
            if action == "quit":
                print(f"{green}[INFO] Quitting vtube.py...{reset}")
                exit()
            try:
                hotkey = MAP[action]
                print(f"{green}[INFO] Hotkey found{reset}")
                open("action.txt", "w").close() # reset file
            except KeyError:
                print("\033[91m[ERROR]\033[00m Cannot find 'action.txt'")
                open("action.txt", "w").close()
                continue
            

            print(f"{green}[INFO] Read action {action} to 'action.txt', sending hotkey request...{reset}")
            send_hotkey_request = vts.vts_request.requestTriggerHotKey(hotkey)
            await vts.request(send_hotkey_request) 
            print(f"{green}[INFO] Received hotkey request{reset}")

        # to sleep the connection running
        response_data = await vts.request(vts.vts_request.requestHotKeyList())
        sleep(1)
        x += 1
        print(f"{green}[INFO] VTS Websockets Connection Tick: {x}{reset}")
        
    await vts.close()

if __name__ == "__main__":
    asyncio.run(main())