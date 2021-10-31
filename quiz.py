import sqlite3
import argparse
import requests
import json
import csv
import time
import os.path

# take a command line variable with a single stock ticker, like AMZN, MSFT, or GOOG
parser = argparse.ArgumentParser()

parser.add_argument("-s", "--stock", dest = "stock", default = "ORCL", help = "Separated by commas")
args = parser.parse_args()

stock = args.stock
apikey = "5teZ6NZ5nvaW0gBEQUT0f40yDqsKCw7I2qpIe7uF"

url = "https://yfapi.net/v6/finance/quote"

querystring = {"symbols" : stock}

headers = {
    'x-api-key': apikey
    }

response = requests.request("GET", url, headers=headers, params=querystring)

response.raise_for_status()  # raises exception when not a 2xx response
if response.status_code != 204:
	stock_json = response.json()

try:
	regular_market_time = stock_json['quoteResponse']['result'][0]["regularMarketTime"]
	regular_market_time_converted = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(regular_market_time))
	print(stock_json['quoteResponse']['result'][0]["shortName"] + ": Current Price:$" + str(stock_json['quoteResponse']['result'][0]["regularMarketPrice"]) + ". " + "Market Time: " + regular_market_time_converted)

	data = [stock, regular_market_time_converted, str(stock_json['quoteResponse']['result'][0]["regularMarketPrice"])]
	if os.path.exists('stock.csv') == False:
		print("CSV file path does not exist.")
	else:
		with open('stock.csv', 'a', encoding='UTF8') as f:
			writer = csv.writer(f)
			writer.writerow(data)
except KeyError:
	print("An unknown stock ticker was entered, so the information wasn't available.")

