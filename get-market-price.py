import requests

ticker = "KXBTCD-25DEC0817-T91499.99"

r = requests.get(f"https://api.elections.kalshi.com/trade-api/v2/markets/{ticker}")
response = r.json()

market = response['market']
print(market['title'])
print(f"BUY YES: {market['yes_ask']}")
print(f"BUY NO: {market['no_ask']}")
print(f"VOLUME: {market['volume_24h']}")