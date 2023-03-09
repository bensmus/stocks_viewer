from dotenv import load_dotenv
import os
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

load_dotenv()
API_KEY = os.getenv('API_KEY')

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey={API_KEY}'
response = requests.get(url)
time_series = response.json()['Time Series (Daily)'] # time_series is a python dictionary

times = list(time_series.keys())[::-1]
day_infos = list(time_series.values())[::-1]

def from_day_infos(key):
    return [float(day_info[key]) for day_info in day_infos]

adjusted_close_prices = from_day_infos('5. adjusted close')
volume = from_day_infos('6. volume')

fig, (ax) = plt.subplots(figsize=(10, 7))
# plt.plot(times, volume)
plt.plot(times, adjusted_close_prices)

step = 10
plt.xticks(range(0, len(adjusted_close_prices), step), list(times)[::step])

# Rotates and right-aligns the x labels so they don't crowd each other.
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')

plt.show()
