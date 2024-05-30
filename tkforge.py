import os
import argparse
from tk import tk_code
from colorama import Fore, init
from urllib.parse import urlparse
from utils import extract_figma_id

init(autoreset=True)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Drag & drop in Figma to create a Python GUI with ease! Donate: " + Fore.BLUE + "https://patreon.com/axorax" + Fore.RESET)

    parser.add_argument('--id', type=str, help="Figma file ID or URL")
    parser.add_argument('--token', type=str, help="Figma token")
    parser.add_argument('--out', type=str, help="Output file path")

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

    return args.id, args.token, args.out

def main():
    file_id, token, output = parse_arguments()
    
    if not file_id or not token:
        print(Fore.RED + "Provide both arguments id and token")
        return

    print(Fore.YELLOW + "Processing...")
    code = tk_code(extract_figma_id(file_id), token, output)

    if code == None:
        print(Fore.RED + "The file ID, token or output path that you provided is invalid!")
    else:
        print(Fore.GREEN + "Success! Your code has been generated!")

if __name__ == "__main__":
    main()
