import os
import sys
import colorama
import ctypes
import requests
import json
import time


alphabet_to_flag = {
    'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫', 'g': '🇬',
    'h': '🇭', 'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳',
    'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹', 'u': '🇺',
    'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾', 'z': '🇿'
}

def logo():
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(f'[Mass Group Manager] | Ready for use <3')
    print(f"""{colorama.Fore.RESET}{colorama.Fore.LIGHTMAGENTA_EX}
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    support
    https://nekodesudx.github.io/aarr/

    created by AARR
    {colorama.Fore.LIGHTCYAN_EX}
    [1] Clean unknown group IDs list
    [2] Reaction spammer
    [3] Exit

    {colorama.Fore.RESET}
    """)

def get_session(proxy=None):
    session = requests.Session()
    if proxy:
        session.proxies = {"http": proxy, "https": proxy}
    return session

def get_headers(session):
    return {
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 OPR/81.0.4196.31"
    }

def reactionput(token, channelid, messageid, emoji, proxy=None):
    session = get_session(proxy)
    headers = get_headers(session)
    headers["Authorization"] = token
    
    emoji = requests.utils.quote(emoji)
    response = session.put(
        f"https://discord.com/api/v9/channels/{channelid}/messages/{messageid}/reactions/{emoji}/%40me?location=Message&type=0",
        headers=headers
    )
    if response.status_code in [200, 204]:
        print(f"[+] Reaction '{emoji}' added successfully to message {messageid}")
    elif response.status_code == 429:
        print("[-] Rate limited. Please wait before retrying.")
        retry_after = response.json().get("retry_after", 1)
        time.sleep(retry_after)  
    elif response.status_code == 401:
        print("[-] Invalid or expired token.")
    else:
        print(f"[!] Error occurred: {response.status_code}")

def fetch_messages(token, channelid, limit=100):
    headers = {
        "Authorization": token,
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 OPR/81.0.4196.31"
    }
    response = requests.get(
        f"https://discord.com/api/v9/channels/{channelid}/messages?limit={limit}",
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"[!] Failed to fetch messages. HTTP Status Code: {response.status_code}")
        return []

def reaction_spammer():
    try:
        with open("config.json") as conf:
            config = json.load(conf)
            token = config["token"]
    except (FileNotFoundError, KeyError):
        print(f"{colorama.Fore.RED}    [!] Error: Config file or token not found!{colorama.Fore.RESET}")
        return

   
    try:
        with open("channel.txt", "r") as channel_file:
            channel_ids = [line.strip() for line in channel_file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{colorama.Fore.RED}    [!] Error: channel.txt file not found!{colorama.Fore.RESET}")
        return

    emoji_input = input("select your emoji (a, b, c, ... or custom emojis): ").strip()
    delay = input("Delay between reactions (in seconds)?: ").strip()

    try:
        delay = float(delay)
        if delay < 0:
            raise ValueError
    except ValueError:
        print(f"{colorama.Fore.RED}    [!] Invalid delay. Using default delay of 1 second.{colorama.Fore.RESET}")
        delay = 1.0

    emojis = []
    for emoji in emoji_input.split(","):
        emoji = emoji.strip().lower()
        if emoji in alphabet_to_flag:
            emojis.append(alphabet_to_flag[emoji]) 
        else:
            emojis.append(emoji)  

    if not emojis:
        print(f"{colorama.Fore.RED}    [!] No valid emojis provided!{colorama.Fore.RESET}")
        return

    
    for channel_id in channel_ids:
        print(f"{colorama.Fore.LIGHTCYAN_EX}Processing channel {channel_id}...{colorama.Fore.RESET}")
        messages = fetch_messages(token, channel_id, limit=100)
        if not messages:
            print(f"{colorama.Fore.RED}    [!] No messages found in the channel or an error occurred.{colorama.Fore.RESET}")
            continue

        for message in messages:
            for emoji in emojis:
                reactionput(token, channel_id, message['id'], emoji)
                time.sleep(delay)

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
            reaction_spammer()
        elif option == "3":
            print(f"{colorama.Fore.LIGHTGREEN_EX}    [*] Exiting the application. Goodbye!{colorama.Fore.RESET}")
            break
        else:
            print(f"{colorama.Fore.RED}    [!] Invalid option selected!{colorama.Fore.RESET}")

        input(f"{colorama.Fore.LIGHTCYAN_EX}Press Enter to return to the main menu...{colorama.Fore.RESET}")

if __name__ == "__main__":
    main()
