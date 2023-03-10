from dotenv import load_dotenv
import os
import requests
import matplotlib.pyplot as plt
import re

load_dotenv()
API_KEY = os.getenv('API_KEY')


def symbol_search(keyword):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={API_KEY}'
    response = requests.get(url)
    symbol_matches = response.json()['bestMatches']

    search_result = {}
    for symbol_match in symbol_matches:
        search_result[symbol_match['1. symbol']] = {
            'name': symbol_match['2. name'],
            'type': symbol_match['3. type'],
            'region': symbol_match['4. region']
        }
    
    return search_result
    

def price_volume_png(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}'

    response = requests.get(url)
    time_series = response.json()['Time Series (Daily)'] # time_series is a python dictionary

    times = list(time_series.keys())[::-1]
    day_infos = list(time_series.values())[::-1] # list of dictionaries [{high: h1, low: l1 ...}, {high: h2, low: l2 ...} ...]
    get_y = lambda key: [float(day_info[key]) for day_info in day_infos]
    adjusted_close = get_y('5. adjusted close')
    volume = get_y('6. volume')

    fig, ax1 = plt.subplots(figsize=(10, 7))
    plt.title('Adjusted close and volume')

    step = 10
    plt.xticks(range(0, len(times), step), list(times)[::step])
    # Rotates and right-aligns the x labels so they don't crowd each other.
    for label in ax1.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')

    color = 'tab:red'
    ax1.set_ylabel('adjusted close', color=color)
    ax1.plot(times, adjusted_close, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('volume', color=color) # we already handled the x-label with ax1
    ax2.plot(times, volume, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.savefig('plot.png')


# print(symbol_search('Taiwan Semiconductor'))
# price_volume_png('IBM')
