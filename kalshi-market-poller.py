import requests
import time
from datetime import datetime
import csv
import os

TICKER = "KXNHLGAME-25DEC09COLNSH-COL"
URL = f"https://api.elections.kalshi.com/trade-api/v2/markets/{TICKER}"
POLL_INTERVAL = 0.1 #seconds
FILENAME= "input.csv"


def poll_market():
    r = requests.get(URL)
    response = r.json()
    market = response['market']

    return {
        'timestamp': datetime.now().isoformat(),
        'ticker': market['ticker'],
        'title': market['title'],
        'yes_ask': market['yes_ask'],
        'no_ask': market['no_ask'],
        'no_bid': market['no_bid'],
        'yes_bid': market['yes_bid'],

    }


previous_price = None

# Write headers only if file doesn't exist
if not os.path.exists(FILENAME):
    with open(FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'yes_ask', 'no_ask'])

# Polling loop
previous_price = (0, 0) # tuple of previous price (yes, no)
poll_count = 0

while True:
    time.sleep(POLL_INTERVAL)

    try:
        data = poll_market()
        #print(f"[{data['timestamp'][11:23]}] Yes: {data['yes_ask']} No: {data['no_ask']}")
    except Exception as e:
        print(f"[ERROR {datetime.now().strftime('%H:%M:%S')}] {e}")
        continue  # Skip this iteration, try again next time

    yes_ask = data['yes_ask']
    no_ask = data['no_ask']

    poll_count += 1
    
    #if (yes_ask, no_ask) == previous_price:
        # Heartbeat every 100 polls (50 seconds) to show it's alive
        #if poll_count % 100 == 0:
            #print(f"[{data['timestamp'][11:23]}] Still polling... (Yes: {yes_ask} No: {no_ask} - unchanged)")
        #continue
    
    print(f"[{data['timestamp'][11:23]}] Yes: {yes_ask} No: {no_ask}")

    # a is append
    with open(FILENAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([data['timestamp'], yes_ask, no_ask])
    
    #previous_price = (yes_ask, no_ask)  # Update for next comparison
