from urllib.parse import urlencode,quote
from weakref import proxy
import requests, time, random, json

#Forward Steam API request trhough Proxy or Broswer Renderer
def steamapi(request, loop_errors = 0):
    #Check correct request arguments
    if request.args and 'market_hash_name' in request.args:
        if 'appid' in request.args:
            appid = str(request.args.get('appid'))
        else:
            appid = str(730)
        #Contruct API request URL from given arguments
        url = "https://steamcommunity.com/market/priceoverview/?appid="+appid+"&currency=3&market_hash_name="+request.args.get('market_hash_name')
        
        #Give up if there are too meny errors
        if loop_errors >= 10: return f'Too many errors'

        try:
            #Randomly decide if we are going to use Proxy or Renderer for the API request
            if random.randint(0,1):
                rand_proxy = randProxy()
                rand_renderer = None
                steam_request = requests.get(url,proxies={"http"  : rand_proxy,"https" : rand_proxy})
            else:
                rand_proxy = None
                rand_renderer = randRenderer()
                steam_request = requests.get(rand_renderer+"/?url="+quote(url))

            #Check valid response. If not ok, wait and try again
            if "€" not in steam_request.text or "{" not in steam_request.text:
                print("Invalid response: "+steam_request.text)
                time.sleep(random.uniform(0, 5))
                return steamapi(request,loop_errors+1)
            else:
                #Prettify response
                response = steam_request.text.replace(',--', '')
                response = response[response.index("{"):response.index("}")+1]
                response = json.loads(response)
                print("Returned price: "+response["lowest_price"]+" Request: "+appid+" "+request.args.get('market_hash_name')+" Proxy: "+str(rand_proxy)+" Renderer: "+str(rand_renderer))
                return response

        #Log possible errors. Wait and try again
        except Exception as e:
            print(e)
            print("Exception. Steam response: "+steam_request.text)
            time.sleep(random.uniform(0, 5))
            return steamapi(request,loop_errors+1)

    else:
        return f'Invalid argument'

#Get random Proxy from file
def randProxy():
    with open("proxies.txt") as f:
        proxies = f.read().splitlines()
    proxies.append(None)
    return random.choice(proxies)

#Get random Renderer from file
def randRenderer():
    with open("urls.txt") as f:
        urls = f.read().splitlines()
    return random.choice(urls)

#####GOOGLE FUNCTION END######
#A partir de aqui, quiitar antes de añadir a Google Functions
class Request_steamapi(object):
    
    def __init__(self, market_hash_name, appid):
        self.args = {'market_hash_name': market_hash_name, 'appid':appid}