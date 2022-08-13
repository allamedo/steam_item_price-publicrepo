# steam_item_price
Google Cloud Functions proxy for Steam prices API
# How it works
The function makes a request to the Steam prices API through Google Cloud Functions.  
The requests can be routed through:
* A HTTP Proxy from proxies.txt
* A HTML renderer from urls.txt (I'm currently using a [Puppeteer Docker implementation](https://github.com/zenato/puppeteer-renderer))

It returns the Steam prices API resopnse as a Google Cloud Functions HTTP response
