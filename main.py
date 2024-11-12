import os
import sys
import colorama
import ctypes
import requests
import json
import time

def logo():
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(f'[Mass Group Manager] | Ready for use <3')
    print(f"""{colorama.Fore.RESET}{colorama.Fore.LIGHTMAGENTA_EX}
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    support
    https://nekodesudx.github.io/aarr/

    created by AARR
    {colorama.Fore.LIGHTCYAN_EX}
    [1] Clean unknown group IDs
    [2] Exit

    {colorama.Fore.RESET}
    """)

def update_group_ids():
    try:
        with open("config.json") as conf:
            config = json.load(conf)
            token = config["token"]
    except (FileNotFoundError, KeyError):
        print(f"{colorama.Fore.RED}    [!] Error: Config file or token not found!{colorama.Fore.RESET}")
        return

    headers = {
        "Authorization": token,
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 OPR/81.0.4196.31"
    }

    response = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers)
    if response.status_code == 200:
        channels = response.json()
        with open("group_id.txt", "w") as group_id_file:
            for channel in channels:
                if channel['type'] == 3:  
                    group_id_file.write(channel['id'] + '\n')
        print(f"{colorama.Fore.LIGHTGREEN_EX}    [+] Group IDs updated successfully.{colorama.Fore.RESET}")
    else:
        print(f"{colorama.Fore.LIGHTRED_EX}    [!] Failed to retrieve group IDs. HTTP Status Code: {response.status_code}{colorama.Fore.RESET}")

def main():
    colorama.init()
    while True:
        logo()
        option = input(f"{colorama.Fore.LIGHTMAGENTA_EX}    [Final] Select an option from above: ")
        
        if option == "1":
            update_group_ids()
        elif option == "2":
            print(f"{colorama.Fore.LIGHTGREEN_EX}    [*] Exiting the application. Goodbye!{colorama.Fore.RESET}")
            break
        else:
            print(f"{colorama.Fore.RED}    [!] Invalid option selected!{colorama.Fore.RESET}")

        input(f"{colorama.Fore.LIGHTCYAN_EX}Press Enter to return to the main menu...{colorama.Fore.RESET}")

if __name__ == "__main__":
    main()

