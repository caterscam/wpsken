#recode can, but add credit
#!/usr/bin/env python3
import os
import requests
import re
from multiprocessing.dummy import Pool
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Color settings
RED = Fore.RED
GREEN = Fore.GREEN

def set_terminal_title(title):
    """Set the terminal title based on the operating system."""
    if os.name == 'nt':  # Windows
        os.system(f'title wordpress checker dev t.me/devonaji | main channel t.me/caterscam')
    else:  # Unix-like (Linux, macOS)
        print(f'\033]0;wordpress checker dev t.me/devonaji | main channel t.me/caterscam\007', end='')

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Display the banner."""
    print("""
█░█░█ █▀█ █▀█ █▀▄ █▀█ █▀█ █▀▀ █▀ █▀   █▀▀ █▀▄▀█ █▀   █▀▀ █░█ █▀▀ █▀▀ █▄▀ █▀▀ █▀█
▀▄▀▄▀ █▄█ █▀▄ █▄▀ █▀▀ █▀▄ ██▄ ▄█ ▄█   █▄▄ █░▀░█ ▄█   █▄▄ █▀█ ██▄ █▄▄ █░█ ██▄ █▀▄
             channel t.me/caterscam | devel0perz t.me/devonaji

[!] don't use http or hhtps at ur list!
─────────────────────────────────────────────────────────────────────────────────
─────────────────────────────────────────────────────────────────────────────────

    """)

def get_input():
    """Prompt user for file and thread count."""
    while True:
        try:
            file_input = input('[*] Input your list (e.g., sites.txt): ').strip()
            with open(file_input, 'r') as file:
                targets = [line.strip() for line in file]
            break
        except FileNotFoundError:
            print(f'{RED}[!] File not found. Please try again.{Style.RESET_ALL}')
        except Exception as e:
            print(f'{RED}[!] Error reading file: {e}{Style.RESET_ALL}')
    
    while True:
        try:
            thread_input = input('[*] Input your threads (e.g., 10): ').strip()
            threads = int(thread_input)
            if threads <= 0:
                raise ValueError("Thread count must be positive.")
            break
        except ValueError as e:
            print(f'{RED}[!] Invalid input for threads: {e}. Please enter a positive integer.{Style.RESET_ALL}')
    
    return targets, threads

def format_url(url):
    """Ensure the URL starts with http:// or https:// and does not end with a slash."""
    if url.endswith('/'):
        url = url.rstrip('/')
    if not url.startswith(('http://', 'https://')):
        url = f"http://{url}"
    return url

def identify_cms(site):
    """Identify CMS from the given site URL."""
    pattern = re.compile('<meta name="generator" content="(.*)" />')
    try:
        site = format_url(site)
        response = requests.get(site, timeout=15)
        response.raise_for_status()
        src = response.text

        if re.search(pattern, src):
            generator = re.findall(pattern, src)[0]
            if 'WordPress' in generator:
                print(f'{site} --> {GREEN}[WordPress]{Style.RESET_ALL}')
                with open('wordpress.txt', 'a') as file:
                    file.write(f'{site}/\n')
            else:
                identify_other(src, site)
        else:
            identify_other(src, site)
    except requests.RequestException:
        print(f'{site} --> {RED}[Time Out]{Style.RESET_ALL}')

def identify_other(src, site):
    """Identify other systems based on source code patterns."""
    if '/wp-content/themes' in src:
        print(f'{site} --> {GREEN}[WordPress]{Style.RESET_ALL}')
        with open('wordpress.txt', 'a') as file:
            file.write(f'{site}/\n')
    elif '/blog/wp-content/' in src:
        print(f'{site} --> {GREEN}[WordPress]{Style.RESET_ALL}')
        with open('wordpress.txt', 'a') as file:
            file.write(f'{site}/\n')
    elif '/site/wp-content/' in src:
        print(f'{site} --> {GREEN}[WordPress]{Style.RESET_ALL}')
        with open('wordpress.txt', 'a') as file:
            file.write(f'{site}/\n')
    elif '/wp/wp-content/' in src:
        print(f'{site} --> {GREEN}[WordPress]{Style.RESET_ALL}')
        with open('wordpress.txt', 'a') as file:
            file.write(f'{site}/\n')
    elif '/wordpress/wp-content/' in src:
        print(f'{site} --> {GREEN}[WordPress]{Style.RESET_ALL}')
        with open('wordpress.txt', 'a') as file:
            file.write(f'{site}/\n')
    else:
        print(f'{site} --> {RED}[Other]{Style.RESET_ALL}')

def main():
    """Main function to get inputs and start processing."""
    clear_screen()  # Clear the terminal screen
    set_terminal_title("WordPress Checker - Dev t.me/devonaji | Main Channel t.me/caterscam")  # Set terminal title
    display_banner()  # Display the banner
    targets, threads = get_input()  # Get user input
    
    # Create a pool of worker threads
    with Pool(threads) as pool:
        pool.map(identify_cms, targets)
    
    print(f'{GREEN}[+] Scanning complete.{Style.RESET_ALL}')

if __name__ == '__main__':
    main()
