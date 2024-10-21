import requests
import threading
import queue
import time

# Banner
banner = """
                      _                                                         _                _                
                     | |                                                       | |              | |               
 _ _ _  ___   ____ _ | |____   ____ ____  ___  ___     ____ ____   ___     ____| | _   ____ ____| |  _ ____  ____ 
| | | |/ _ \ / ___) || |  _ \ / ___) _  )/___)/___)   / ___)    \ /___)   / ___) || \ / _  ) ___) | / ) _  )/ ___)
| | | | |_| | |  ( (_| | | | | |  ( (/ /|___ |___ |  ( (___| | | |___ |  ( (___| | | ( (/ ( (___| |< ( (/ /| |    
 \____|\___/|_|   \____| ||_/|_|   \____|___/(___/    \____)_|_|_(___/    \____)_| |_|\____)____)_| \_)____)_|    
                       |_| code dev @devonaji | pub channel : @caterscam > version 2 [sett ur UA and threads]                                                                                        
"""

# Set global variables
threads = 30
timeout_duration = 10

# Custom User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0'
}

# Queue for processing websites
q = queue.Queue()

# Function to check CMS of a website
def check_wordpress(site):
    # Add http if not present
    if not site.startswith('http://') and not site.startswith('https://'):
        site = 'http://' + site

    try:
        # Check /wp-json first
        response = requests.get(site + "/wp-json", headers=headers, timeout=timeout_duration)
        if response.status_code == 200:
            print(f"[ wordpress ] {site}")
            with open(outputfile, "a") as wp_file:
                wp_file.write(site + "\n")
            return

        # Check /xmlrpc.php if /wp-json fails
        response = requests.get(site + "/xmlrpc.php", headers=headers, timeout=timeout_duration)
        if response.status_code == 200:
            print(f"[ wordpress ] {site}")
            with open(outputfile, "a") as wp_file:
                wp_file.write(site + "\n")
            return

        # If both checks fail, consider it "other"
        print(f"[ other ] {site}")

    except requests.exceptions.Timeout:
        print(f"[ time out ] {site}")
    except requests.exceptions.RequestException:
        print(f"[ other ] {site}")

# Worker function for threading
def worker():
    while not q.empty():
        site = q.get()
        check_wordpress(site)
        q.task_done()

# Main function
def main():
    global outputfile  # Use global to modify the output file within the function
    
    # Display banner
    print(banner)

    # Ask for input file and output file
    inputlist = input("[*] list sites want to checker wordpress : ")
    outputfile = input("[*] save the result of wordpress cms : ")

    print(f"[+] scanning started for sites listed in: {inputlist}")
    
    # Read sites from input list
    with open(inputlist, "r") as file:
        sites = file.readlines()
    
    # Add each site to the queue
    for site in sites:
        site = site.strip()
        q.put(site)
    
    # Create thread workers
    for i in range(threads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
    
    # Wait for all threads to finish
    q.join()
    print(f"[+] Scanning complete. Results saved to: {outputfile}")

if __name__ == "__main__":
    main()

