import os
import argparse
from tk import tk_code
from colorama import Fore, init
from utils import extract_figma_id, has_update, VERSION

init(autoreset=True)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Drag & drop in Figma to create a Python GUI with ease! Donate: " + Fore.BLUE + "https://patreon.com/axorax" + Fore.RESET)

    parser.add_argument('--id', type=str, help="Figma file/design ID or URL")
    parser.add_argument('--token', type=str, help="Figma token")
    parser.add_argument('--out', type=str, help="Output file path")
    
    parser.add_argument('--update', action='store_true', help="Check for updates")
    parser.add_argument('--version', '-v', action='store_true', help="Display the current version")

    parser.add_argument('args', nargs='*', help="id token output-path")
    
    args = parser.parse_args()

    if not any([args.id, args.token]) and args.args:
        if len(args.args) == 2:
            args.id, args.token = args.args
            args.out = None
        elif len(args.args) == 3:
            args.id, args.token, args.out = args.args

    if args.out == '.':
        args.out = os.getcwd()

    return args

def main():
    args = parse_arguments()

    if args.update:
        try:
            update = has_update()
            if update == False:
                print(Fore.GREEN + "No updates!")
            else:
                print("New update!\nUpdate your version of TkForge to get the latest features!\nhttps://github.com/axorax/tkforge/releases")
        except:
            print(Fore.RED + "Update check failed!")
        return

    if args.version:
        print(f"TkForge v{VERSION}")
        return

    file_id, token, output = args.id, args.token, args.out
    
    if not file_id or not token:
        print(Fore.RED + "Provide both arguments id and token. Make sure to wrap URL in quotes(\").")
        return

    print(Fore.YELLOW + "Processing...")
    code = tk_code(extract_figma_id(file_id), token, output)

    if code is None:
        print(Fore.RED + "The file ID, token or output path that you provided is invalid!")
    else:
        print(Fore.GREEN + "Success! Your code has been generated!")

if __name__ == "__main__":
    main()
