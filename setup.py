import os
import argparse
import subprocess
from colors import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--enable_video", default=False, 
                        help = "Enable video or not")
    parser.add_argument("--enable_vtube", default=False,
                        help="Enable websocket connection to VTS or not")
    parser.add_argument("--save_video", default = False, 
                        help = "Save video recording or not")
    args = parser.parse_args()

    args.enable_video = bool(args.enable_video)
    args.enable_vtube = bool(args.enable_vtube)
    args.save_video = bool(args.save_video)
    
    print("========= key ==========")
    print(f"{red}Red is for Errors {reset}")
    print(f"{orange}Orange is for 'main.py' {reset}")
    print(f"{green}Green is for 'vtube.py'{reset}")
    print(f"{cyan}Cyan is for this file")
    print(f"{blue}Blue is for 'video.py'{reset}")
    print(f"{purple}Purple is for 'main_chat.py'{reset}")
    print("========================\n\n")

    # Resetting required files to blank
    print(f"{cyan}[INFO] Resetting output file{reset}")
    os.system("touch output.txt")
    print(f"{cyan}[INFO] Resetting 'action.txt'{reset}")
    os.system("touch action.txt")
    print(f"{cyan}[INFO] Resetting 'emotion.txt'{reset}")
    os.system("touch emotion.txt")
    print(f"{cyan} [INFO] Setting up 'token.txt'{reset}")
    os.system("touch token.txt")

    # Run main python program
    subprocess.Popen(["python", "main.py"])

    # run corresponding programs if flag is set
    if args.enable_video:
        print(f"{cyan}[INFO] Initializing video.py{reset}")
        subprocess.Popen(["python", "video.py", f"--save_video={args.save_video}"])

    if args.enable_vtube:
        print(f"{cyan}[INFO] Initializing vtube.py{reset}")
        subprocess.Popen(["python", "vtube.py"])


if __name__ == '__main__':
    main()