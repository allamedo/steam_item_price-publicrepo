import requests,random
import threading, time
import main

def print_location(index):
    response = requests.get(random.choice(proxy_urls)+"/?url=http://ip-api.com/line/")
    print(str(index)+". "+response.text.splitlines()[1]+"   "+response.text.splitlines()[4])

def print_locations_threaded_loop():
    with open("urls.txt") as f:
        proxy_urls = f.read().splitlines()

    for index in range(0,20):
        threading.Thread(target=main.print_location,args=(index,)).start()

    time.sleep(20)

def stress_test():

    class Request_steamapi(object):
        def __init__(self, market_hash_name, appid):
            self.args = {'market_hash_name': market_hash_name, 'appid':appid}

    def print_request():
        main.steamapi( Request_steamapi('Falchion%20Case',730) )

    for index in range(0,40):
        threading.Thread(target=print_request).start()

    time.sleep(30)
    

if __name__ == "__main__":
    stress_test()