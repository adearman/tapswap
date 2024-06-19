import requests
import json
import time
from colorama import init, Fore, Style
import sys
import os
init(autoreset=True)
import random
import requests
import re
from bs4 import BeautifulSoup

def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "Tapswap BOT")
    print(Fore.GREEN + Style.BRIGHT + "Update Link: https://github.com/adearman/tapswap")
    print(Fore.GREEN + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie\n")
    print(Fore.GREEN + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")



with open('init_data.txt', 'r') as file:
    init_data_lines = file.readlines()

# Fungsi untuk login dan mendapatkan token akses serta shares
def get_access_token_and_shares(init_data_line):
    try:
        chr_value, actual_init_data = init_data_line.split('|')
    except ValueError:
        print("Format baris tidak valid: ", init_data_line)
        return None, None, None, None

    url = "https://api.tapswap.ai/api/account/login"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Origin": "https://app.tapswap.club",
        "Referer": "https://app.tapswap.club/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "x-app": "tapswap_server",
        "x-cv": "629",
        "x-bot": "no",
    }

    payload = {
        "init_data": actual_init_data,
        "referrer": "",
        "chr" : int(chr_value),
        "bot_key": "app_bot_0"
    }
    # print(payload)
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        data = response.json()
        if 'access_token' in data:
            access_token = data['access_token']
            name = data['player']['full_name']
            coin = data['player']['shares']
            energy = data['player']['energy']
            level_energy = data['player']['energy_level']
            level_charge = data['player']['charge_level']
            level_tap = data['player']['tap_level']
            boosts = data['player']['boost']
            energy_boost = next((b for b in boosts if b["type"] == "energy"), None)
            turbo_boost = next((b for b in boosts if b["type"] == "turbo"), None)
            boost_ready = turbo_boost['cnt']
            energy_ready = energy_boost['cnt']

            print(f"{Fore.BLUE+Style.BRIGHT}\n========================== ")  
            print(f"{Fore.GREEN+Style.BRIGHT}[ Nama ]: {name}")    
            print(f"{Fore.YELLOW+Style.BRIGHT}[ Koin ]: {coin:,.0f}".replace(',', '.'))
            print(f"{Fore.YELLOW+Style.BRIGHT}[ Energi ]: {energy}")
            print(f"{Fore.CYAN+Style.BRIGHT}[ Level Tap ]: {level_tap}")
            print(f"{Fore.CYAN+Style.BRIGHT}[ Level Energi ]: {level_energy}")
            print(f"{Fore.CYAN+Style.BRIGHT}[ Level Recharge ]: {level_charge}")
            print(f"{Fore.MAGENTA+Style.BRIGHT}[ Free Booster ] : Energy {energy_boost['cnt']} | Turbo : {turbo_boost['cnt']}")

            return access_token, energy, boost_ready, energy_ready
        else:
            print("Token akses tidak ditemukan dalam respons.")
            return None, None, None, None
    elif response.status_code == 408:
        print("Request Time Out")
    else:
        print(response.json())
        print(f"Gagal mendapatkan token akses, status code: {response.status_code}")
    
    return None, None, None, None
turbo_activated = False    
def apply_turbo_boost(access_token):
    global turbo_activated
    url = "https://api.tapswap.ai/api/player/apply_boost"
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Origin": "https://app.tapswap.club",
            "Referer": "https://app.tapswap.club/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "x-app": "tapswap_server",
            "x-cv": "624",
            "x-bot": "no",
            # "Content-Id": content_id
        }

    
    payload = {"type": "turbo"}
    if turbo_activated == False:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:

            print(f"\r{Fore.GREEN+Style.BRIGHT}Turbo boost berhasil diaktifkan           ", flush=True)
            turbo_activated = True
            return True

        else:
            print(f"{Fore.RED+Style.BRIGHT}Gagal mengaktifkan turbo boost, status code: {response.json()}")
            return False
    else:
        print(f"\r{Fore.GREEN+Style.BRIGHT}Turbo aktif")
        return True



# Fungsi untuk mengirim taps
def upgrade_level(headers, upgrade_type):
    for i in range(5):
        print(f"\r{Fore.WHITE+Style.BRIGHT}Upgrading {upgrade_type} {'.' * (i % 4)}", end='', flush=True)
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Origin": "https://app.tapswap.club",
            "Referer": "https://app.tapswap.club/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "x-app": "tapswap_server",
            "x-cv": "629",
            "x-bot": "no",
            # "Content-Id": content_id
    }
    url = "https://api.tapswap.ai/api/player/upgrade"
    payload = {"type": upgrade_type}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"\r{Fore.GREEN+Style.BRIGHT}Upgrade {upgrade_type} berhasil", flush=True)
        return True
    else:
        response_json = response.json()
        if 'message' in response_json and 'not_enough_shares' in response_json['message']:
            print(f"\r{Fore.RED+Style.BRIGHT}Koin tidak cukup untuk upgrade {upgrade_type}", flush=True)
            return False
        else:
            print(f"\r{Fore.RED+Style.BRIGHT}Error saat upgrade {upgrade_type}: {response_json['message']}", flush=True)
        return False



# Tambahkan input untuk penggunaan booster
use_booster = input("Gunakan booster secara otomatis? (Y/N): ").strip().lower()
if use_booster in ['y', 'n', '']:
    use_booster = use_booster or 'n'
else:
    print("Input tidak valid. Harus 'Y' atau 'N'.")
    sys.exit()


use_upgrade = input("Lakukan upgrade secara otomatis? (Y/N): ").strip().lower()
if use_upgrade in ['y', 'n', '']:
    use_upgrade = use_upgrade or 'n'
else:
    print("Input tidak valid. Harus 'Y' atau 'N'.")
    sys.exit()

use_kyc = input("Auto KYC Task Binance? (Y/N): ").strip().lower()
if use_kyc in ['y', 'n', '']:
    use_kyc = use_kyc or 'n'
else:
    print("Input tidak valid. Harus 'Y' atau 'N'.")
    sys.exit()

# Tambahkan input untuk auto clear task
auto_clear = input("Auto clear task? (Y/N): ").strip().lower()
if auto_clear in ['y', 'n', '']:
    auto_clear = auto_clear or 'n'
else:
    print("Input tidak valid. Harus 'Y' atau 'N'.")
    sys.exit()

auto_claim_league = input("Auto Claim League? (Y/N): ").strip().lower()
if auto_claim_league in ['y', 'n', '']:
    auto_claim_league = auto_claim_league or 'n'
else:
    print("Input tidak valid. Harus 'Y' atau 'N'.")
    sys.exit()

# Kemudian, modifikasi fungsi `submit_taps` untuk memperhitungkan input ini
def submit_taps(access_token, energy, boost_ready, energy_ready, content_id, time_stamp, init_data_line):
    global turbo_activated
    tap_count = 0
    max_upgrade = 0 
    while True:
        url = "https://api.tapswap.ai/api/player/submit_taps"

        if use_booster == 'y':
            if boost_ready > 0:
                if turbo_activated == False:
                    print(f"\r{Fore.WHITE+Style.BRIGHT}Turbo boost ready, applying turbo boost", end='', flush=True)
                    apply_turbo_boost(access_token)
                else:
                    print(f"\r{Fore.WHITE+Style.BRIGHT}Turbo aktif", end='', flush=True)
                    
        if energy < 50:
            print(f"\r{Fore.RED+Style.BRIGHT}Low Energy", end='', flush=True)
            if use_booster == 'y':
                if turbo_activated == False:
                # Cek ketersediaan energy boost
                    if energy_ready > 0 :
                        print(f"\r{Fore.WHITE+Style.BRIGHT}Energy boost ready, applying energy boost", end='', flush=True)
                        apply_energy_boost(access_token,content_id,time_stamp) 
                        cek_energy = 100
            else:
                time.sleep(3)

                print(f"\r{Fore.RED+Style.BRIGHT}Beralih ke akun selanjutnya", end='', flush=True)
                return
                access_token, energy, boost_ready = get_access_token_and_shares(init_data_line)          
        else:
            print(f"\r{Fore.WHITE+Style.BRIGHT}[ Tap ] : Tapping ..", end='', flush=True)

        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {access_token}",
            "Connection": "keep-alive",
            "Content-Id": content_id,
            "Content-Type": "application/json",
            "Origin": "https://app.tapswap.club",
            "Referer": "https://app.tapswap.club/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "x-app": "tapswap_server",
            "x-bot": "no",
            "x-cv": "624",
        }

        if turbo_activated == True:
            total_taps = random.randint(20, 30)
            payload = {"taps": total_taps, "time": int(time_stamp)}
        else:
            total_taps = random.randint(20, 30)
            payload = {"taps": total_taps, "time": int(time_stamp)}

       

        if turbo_activated == True:
            for _ in range(20):
                time.sleep(2)
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 201:
                    print(f"\r{Fore.GREEN+Style.BRIGHT}[ Tap ] : Tapped              ", flush=True)
                else:
                    print(f"\r{Fore.RED+Style.BRIGHT}[ Tap ] : Gagal mengirim taps, status code: {response.status_code}")
            turbo_activated = False
        else:
            time.sleep(1)
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                print(f"\r{Fore.GREEN+Style.BRIGHT}[ Tap ] : Tapped            ", flush=True)
                tap_count += 1
                
                if tap_count == 20:
                    print(f"\r{Fore.YELLOW+Style.BRIGHT}[ Tap ] : Tapped 20x, ganti akun", flush=True)
                    return
                if use_upgrade == 'y' :
                    max_upgrade += 1
                    # upgrade_level(headers, "tap")
                    # upgrade_level(headers, "energy")
                    if max_upgrade < 6:
                        time.sleep(1)
                        up_charge = upgrade_level(access_token, upgrade_type="charge")
                        if up_charge == False:
                            print(f"\r{Fore.RED+Style.BRIGHT}Recharge sudah level max", flush=True)
                            max_upgrade = 6
                cek_energy = response.json().get("player").get("energy")
                if cek_energy < 50:
                    if use_booster == 'y':
                    # Cek ketersediaan energy boost
                        if energy_ready > 0 :
                            print(f"\r{Fore.WHITE+Style.BRIGHT}Energy boost ready, applying energy boost", end='', flush=True)
                            apply_energy_boost(access_token,content_id,time_stamp)  
                    # print(f"\r{Fore.RED+Style.BRIGHT}[ Tap ] : Energi rendah, memeriksa akun lain\n", flush=True)
                    return
            else:
                print(f"\n\r{Fore.RED+Style.BRIGHT}Gagal mengirim taps, status code: {response.text}")
                print(f"\r{Fore.RED+Style.BRIGHT}Beralih ke akun selanjutnya", end='', flush=True)
                return
            
            
def claim_league(access_token, league_id):
    url = "https://api.tapswap.ai/api/player/claim_reward"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Origin": "https://app.tapswap.club",
        "Referer": "https://app.tapswap.club/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "x-app": "tapswap_server",
        "x-bot": "no",
        "x-cv": "623"
    }
    payload = {"task_id": "L"+str(league_id)}
 
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"{Fore.GREEN+Style.BRIGHT}\r[ League {league_id} ] : Klaim berhasil", flush=True)
        return True
    else:
        response_json = response.json()
        if response_json.get("message") == "player_claim_not_found":
            print(f"{Fore.RED+Style.BRIGHT}\r[ League {league_id} ] : Gagal / Already Claim", flush=True)
            return False
        print(f"{Fore.RED+Style.BRIGHT}\r[ League {league_id} ] : Gagal klaim liga, status code: {response.text}", flush=True)
        return False

 
#Fungsi untuk join mission
def join_mission(access_token, mission_id):
    url = "https://api.tapswap.ai/api/missions/join_mission"
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Origin": "https://app.tapswap.club",
            "Referer": "https://app.tapswap.club/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "x-app": "tapswap_server",
            "x-cv": "624",
            "x-bot": "no",
            # "Content-Id": content_id
        }
    payload = {"id": mission_id}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"{Fore.GREEN+Style.BRIGHT}\r[ KYC ] : Mengaktifkan {mission_id}", flush=True)
        return True
    else:
        response = response.json()
        if response.get("message") == "mission_already_completed":
            print(f"{Fore.GREEN+Style.BRIGHT}\r[ KYC ] : Sudah KYC", flush=True)
            claim_reward(access_token, mission_id)
            return False
        elif response.get("message") == "mission_already_joined":
            print(f"{Fore.GREEN+Style.BRIGHT}\r[ KYC ] : Proses KYC", flush=True)
            return True
        print(f"{Fore.RED+Style.BRIGHT}\r[ KYC ] : Gagal mengaktifkan {mission_id}, status code: {response.text}", flush=True)
        return False
def auto_clear_task(access_token, mission_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Origin": "https://app.tapswap.club",
        "Referer": "https://app.tapswap.club/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "x-app": "tapswap_server",
        "x-cv": "629"
    }
    for _ in range(2):  # Ulangi 2 kali
        for item_index in range(3):  # Untuk index 0, 1, 2
            payload = {"id": mission_id, "itemIndex": item_index}
            response = requests.post("https://api.tapswap.ai/api/missions/finish_mission_item", headers=headers, json=payload)
            if response.status_code == 201:
                print(f"{Fore.GREEN+Style.BRIGHT}\r[ Task ] Item {item_index} misi {mission_id} berhasil diselesaikan.", flush=True)
            else:
                print(f"{Fore.RED+Style.BRIGHT}\r[ Task ] Gagal menyelesaikan item {item_index} misi {mission_id}, status code: {response.status_code}", flush=True)

# Fungsi untuk menyelesaikan item misi
def finish_mission_item(access_token, mission_id, item_index, user_input=None):
    url = "https://api.tapswap.ai/api/missions/finish_mission_item"
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Origin": "https://app.tapswap.club",
            "Referer": "https://app.tapswap.club/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "x-app": "tapswap_server",
            "x-cv": "624",
            "x-bot": "no",
            # "Content-Id": content_id
        }
    payload = {"id": mission_id, "itemIndex": item_index}
    if user_input:
        payload["user_input"] = user_input
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"{Fore.GREEN+Style.BRIGHT}\r[ KYC ] : Menyelesaikan {mission_id}", flush=True)
        return True
    else:
        response = response.json()
        if response.get("message") == "mission_not_found":
            print(f"{Fore.GREEN+Style.BRIGHT}\r[ KYC ] : Sudah menyelesaikan {mission_id}", flush=True)
            return True
        elif response.get("message") == "mission_item_already_verified":
            print(f"{Fore.GREEN+Style.BRIGHT}\r[ KYC ] : Sudah menyelesaikan {mission_id}", flush=True)
            return True
        elif response.get("message") == "mission_items_not_finished":
            print(f"{Fore.RED+Style.BRIGHT}\r[ KYC ] : Item misi belum selesai, mengulangi...", flush=True)
            return False
        else:
            print(f"{Fore.RED+Style.BRIGHT}\r[ KYC ] : Gagal menyelesaikan {mission_id} {response}", flush=True)
            return False    
    
# Fungsi untuk menyelesaikan misi
def finish_mission(access_token, mission_id):
    url = "https://api.tapswap.ai/api/missions/finish_mission"
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Origin": "https://app.tapswap.club",
            "Referer": "https://app.tapswap.club/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "x-app": "tapswap_server",
            "x-cv": "624",
            "x-bot": "no",
            # "Content-Id": content_id
        }
    payload = {"id": mission_id}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"{Fore.GREEN+Style.BRIGHT}\r[ KYC ] : Menyelesaikan {mission_id}", flush=True)
        return True
    else:
        response = response.json()
        if response.get("message") == "mission_items_not_finished":
            print(f"{Fore.RED+Style.BRIGHT}\r[ KYC ] : Misi {mission_id} belum selesai", flush=True)
            return False
        print(f"{Fore.RED+Style.BRIGHT}\r[ KYC ] : Gagal menyelesaikan {mission_id}, status code: {response.text}", flush=True)
        return False
# Fungsi untuk klaim reward
def claim_reward(access_token, task_id):
    url = "https://api.tapswap.ai/api/player/claim_reward"
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Origin": "https://app.tapswap.club",
            "Referer": "https://app.tapswap.club/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "x-app": "tapswap_server",
            "x-cv": "624",
            "x-bot": "no",
            # "Content-Id": content_id
        }
    payload = {"task_id": task_id}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"{Fore.GREEN+Style.BRIGHT}\r[ KYC ] : Done KYC. Reward 3.000.000 Coins", flush=True)
        return True
    else:
        response = response.json()
        if response.get("message") == "player_claim_not_found":
            print(f"{Fore.RED+Style.BRIGHT}\r[ KYC ] : Gagal KYC. Belum memenuhi syarat", flush=True)
            return False
        print(f"{Fore.RED+Style.BRIGHT}\r[ KYC ] : Gagal KYC, status code: {response.text}", flush=True)
        return False
    
def auto_kyc_binance(access_token, mission_id, binance_id):
    print(f"{Fore.GREEN+Style.BRIGHT}\r[ KYC ] : Mencoba KYC Binance", flush=True)
    if join_mission(access_token, mission_id):
        for item_index in range(3):
            if item_index == 2:
                finish_mission_item(access_token, mission_id, item_index, binance_id)
            else:
                finish_mission_item(access_token, mission_id, item_index)
        finish_mission(access_token, mission_id)
        claim_reward(access_token, mission_id)


def clear_console():

    # Clear the console based on the operating system
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
def apply_energy_boost(access_token, content_id, timestamp):

    url = "https://api.tapswap.ai/api/player/apply_boost"
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Origin": "https://app.tapswap.club",
            "Referer": "https://app.tapswap.club/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "x-app": "tapswap_server",
            "x-cv": "624",
            "x-bot": "no",
        }

    payload = {"type": "energy"}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"\r{Fore.GREEN+Style.BRIGHT}Energy boost berhasil diaktifkan                 ", flush=True)
        submit_taps(access_token, 100, 0, 0, content_id, timestamp, init_data_line)  # Anggap energy penuh setelah boost
        return True

    else:
        print(f"{Fore.RED+Style.BRIGHT}Gagal mengaktifkan energy boost, status code: {response.status_code}")
        return False
import urllib.parse
import json
while True:  # Loop ini akan terus berjalan sampai skrip dihentikan secara manual
    print_welcome_message()
    for init_data_line in init_data_lines:
        init_data_line = init_data_line.strip()
        query_params = urllib.parse.parse_qs(init_data_line)
        user_data = query_params.get('user', [None])[0]
        #access_token, energy, boost_ready, energy_ready = get_access_token_and_shares(init_data_line.strip())  # Terima energy_boost
        if user_data:
                user_data_json = json.loads(urllib.parse.unquote(user_data))
                user_id = user_data_json.get('id')
                
                if user_id:
                    timestamp = int(time.time() * 1000)
                    content_id = int((timestamp * user_id * user_id / user_id) % user_id % user_id)
                    
                 
                    
                    access_token, energy, boost_ready, energy_ready = get_access_token_and_shares(init_data_line)
                    if access_token is None:
                        print(f"\r{Fore.RED+Style.BRIGHT}Token akses tidak valid, lanjut ke akun berikutnya.", flush=True)
                        continue

                    # if use_upgrade == 'y':
                    #     if random.random() < 0.5:
                    #         upgrade_level(headers={"Authorization": f"Bearer {access_token}"}, upgrade_type="energy")
                    #     else:
                    #         upgrade_level(headers={"Authorization": f"Bearer {access_token}"}, upgrade_type="tap")

                    if auto_claim_league == 'y':
                        for id_liga in range(1, 9):
                            claim_league(access_token, id_liga)

                    if use_kyc == 'y':
                        binance_id = str(random.randint(10000000, 99999999))
                        auto_kyc_binance(access_token, "M34", binance_id)
                    
                    if auto_clear == 'y':
                        mission_id = "M0"  # Ganti dengan ID misi yang valid
                        auto_clear_task(access_token, mission_id)
                        claim_reward(access_token, mission_id)

        submit_taps(access_token, energy, boost_ready, energy_ready, str(content_id), timestamp, init_data_line)
        time.sleep(random.uniform(1.5, 3.0))  # Kirim energy_boost ke submit_taps
    
    print(f"\n\n{Fore.CYAN+Style.BRIGHT}==============Semua akun telah diproses=================\n")
    for detik in range(60, 0, -1):
        print(f"\rMemulai lagi dalam {detik} detik...", end='')
        time.sleep(1)
    clear_console()
