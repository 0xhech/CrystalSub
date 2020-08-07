# Developing by AsafDamn github: github.com/AsafDamn


# Modules

import requests
from threading import Thread
from queue import Queue
from colored import fg, attr

#Colors

color1 = fg('magenta')
color2 = fg("green")
color3 = fg("dark_slate_gray_1")
color4 = fg("red")
color5 = fg("pale_green_3a")
color6 = fg("blue")
res = attr('reset')
#Thanks to my friend İlker for helping me with the coloring.

# Banner

intro = """

                                                                                                                                                                                        
                                                                                                                                                                                                                
  ▄████▄   ██▀███ ▓██   ██▓  ██████ ▄▄▄█████▓ ▄▄▄       ██▓      ██████  █    ██  ▄▄▄▄   
▒██▀ ▀█  ▓██ ▒ ██▒▒██  ██▒▒██    ▒ ▓  ██▒ ▓▒▒████▄    ▓██▒    ▒██    ▒  ██  ▓██▒▓█████▄ 
▒▓█    ▄ ▓██ ░▄█ ▒ ▒██ ██░░ ▓██▄   ▒ ▓██░ ▒░▒██  ▀█▄  ▒██░    ░ ▓██▄   ▓██  ▒██░▒██▒ ▄██
▒▓▓▄ ▄██▒▒██▀▀█▄   ░ ▐██▓░  ▒   ██▒░ ▓██▓ ░ ░██▄▄▄▄██ ▒██░      ▒   ██▒▓▓█  ░██░▒██░█▀  
▒ ▓███▀ ░░██▓ ▒██▒ ░ ██▒▓░▒██████▒▒  ▒██▒ ░  ▓█   ▓██▒░██████▒▒██████▒▒▒▒█████▓ ░▓█  ▀█▓
░ ░▒ ▒  ░░ ▒▓ ░▒▓░  ██▒▒▒ ▒ ▒▓▒ ▒ ░  ▒ ░░    ▒▒   ▓▒█░░ ▒░▓  ░▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░▒▓███▀▒
  ░  ▒     ░▒ ░ ▒░▓██ ░▒░ ░ ░▒  ░ ░    ░      ▒   ▒▒ ░░ ░ ▒  ░░ ░▒  ░ ░░░▒░ ░ ░ ▒░▒   ░ 
░          ░░   ░ ▒ ▒ ░░  ░  ░  ░    ░        ░   ▒     ░ ░   ░  ░  ░   ░░░ ░ ░  ░    ░ 
░ ░         ░     ░ ░           ░                 ░  ░    ░  ░      ░     ░      ░      
░                 ░ ░                                                                 ░                                                                                                                                                                                         
                                        
                        Subdomain Scanner - Powered By @AsafDamn
                ========================================================                   
        Usage of CrystalSub for attacking targets without prior mutual consent is illegal. 
    It is the end user's responsibility to obey all applicable local, state and federal laws. 
 Developer assume no liability and are not responsible for any misuse or damage caused by this program.

"""
print(intro)
#Thanks to Dude Caner who found the name CrystalSub.

q = Queue()

def scan_subdomains(domain):
    global q
    while True:
        subdomain = q.get()
        url = f"http://{subdomain}.{domain}"
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print( color3 + "[$] Discovered subdomain:" + res  ,url)

        q.task_done()


def main(domain, n_threads, subdomains):
    global q

    for subdomain in subdomains:
        q.put(subdomain)

    for t in range(n_threads):
        worker = Thread(target=scan_subdomains, args=(domain,))
        worker.daemon = True
        worker.start()
    


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description= color6 + "Faster Subdomain Scanner Using Threads" + res  )
    parser.add_argument("domain", help=color6 +"Domain to scan for subdomains without protocol ('http://' or 'https://')"+ res)
    parser.add_argument("-l", "--wordlist", help= color6 + "File that contains all subdomains to scan, line by line." + res,
                        default="subdomains.txt")
    parser.add_argument("-t", "--num-threads", help= color6 +"Number of threads to use to scan the domain. Default is 10", default=10, type=int)
    
    args = parser.parse_args()
    domain = args.domain
    wordlist = args.wordlist
    num_threads = args.num_threads

    try:
        main(domain=domain, n_threads=num_threads, subdomains=open(wordlist).read().splitlines())
        q.join()
    except KeyboardInterrupt:
        print()
        print()
        print( "Bye Bye..!") 
        print()

#Please do not steal the source code ..!