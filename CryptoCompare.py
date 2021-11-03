# import MatPlotLib and Pandas libraries
# also need Requests library, in order to interact with web servers as a client

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import json
import numpy as np

url = "https://min-api.cryptocompare.com/data/v2/histoday"

parametersETH = {'fsym': 'ETH',
            'tsym': 'USD', 
            'aggregate days': 30,
            }

responseEth = requests.get(url, params=parametersETH)
data = responseEth.json()
eth_dic = dict(data['Data'])
    
df_eth = pd.DataFrame(eth_dic['Data'])



parametersBTC = {'fsym': 'BTC',
            'tsym': 'USD' 
            }

response = requests.get(url, params=parametersBTC)
data = response.json()

btc_dic = dict(data['Data'])

df_btc = pd.DataFrame(btc_dic['Data'])

# The above code gets and changes the data from API into a dataframe which keeps price for ETH/USD (df_eth) and BTC/USD (df_btc)
# a. Calculate, which coin performed better over 30 days? Daily Returns

pd.to_datetime(df_eth.time, unit = 's')

closePrice = df_eth['close']
openPrice = df_eth['open']

sum_eth = sum(closePrice)
change30 = (closePrice[30] - closePrice[0]) * 100 / closePrice[0]
change30 = round(change30,ndigits=3)
print('Increase in price of ETH over 30 days is: ' + str(change30) + '%')


daily_eth = (closePrice - openPrice) * 100 / openPrice
avg_eth = sum(daily_eth)/30

print('Daily average increase of ETH/USD, for the last 30 days was: ' + str(avg_eth) + '%')

pd.to_datetime(df_btc.time, unit = 's')

closePriceBtc = df_btc['close']
openPriceBtc = df_btc['open']

sum_btc = sum(closePrice)
change30btc = (closePriceBtc[30] - closePriceBtc[0]) * 100 / closePriceBtc[0]
change30btc = round(change30btc, ndigits=2)



daily_btc = (closePriceBtc - openPriceBtc) * 100 / openPriceBtc

print('Increase in price is: ' + str(change30btc) + '%')
avg_btc = sum(daily_btc)/30

print('Daily average increase of BTC/USD, for the last 30 days was: ' + str(avg_btc) + '%')

# b. What was the average, median and sd of daily returns? (%change for each day)

average_eth = round(sum(daily_eth)/30, ndigits=3)
average_btc = round(sum(daily_btc)/30, ndigits=3)

std_eth = round(np.std(daily_eth), ndigits=3)
std_btc = round(np.std(daily_btc), ndigits=3)

median_eth = np.median(daily_eth)
median_btc = np.median(daily_btc)

print('\n ETH Daily returns average: ', str(average_eth),
'\n BTC Daily returns average: ', str(average_btc), 
'\n ETH Standard deviation: ', str(std_eth), 
'\n BTC Standard deviation: ', str(std_btc),
'\n ETH Median % increase: ', str(median_eth),
'\n BTC Median % increase:', str(median_btc))

# 2. a. gather BTC blockchain data for 30 days, and draw a graph (MatPlotlib)
# api endpoint => https://min-api.cryptocompare.com/documentation?key=Blockchain&cat=blockchainDay

url1 = 'https://min-api.cryptocompare.com/data/blockchain/histo/day?&api_key=4d536cebd563ac5459eabb0ded6ac6d05fcc379ef68e4464ed839ef8281138e8'

parameters = {
    'fsym' : 'BTC'
}

graphBtc = requests.get(url1, params=parameters)

graphJson = graphBtc.json()

graph_btc = pd.DataFrame(graphJson['Data']['Data'])

date = pd.to_datetime(graph_btc['time'], unit='s')
hashrate = graph_btc['hashrate']
date_df = pd.to_datetime(df_eth['time'], unit='s')

# b. Correlation between Price and Hashrate

correlation = closePrice.corr(graph_btc['hashrate'])
print('Correlation of BTC Price to BTC Hashrate is: ', str(correlation))


# The diagram

fig, ax1 = plt.subplots()
ax1.set_title("BTC's Hashrate and Price")
colour = 'tab:red'
ax1.plot(date, hashrate, color = colour)
fig.autofmt_xdate()

ax1.set_ylim(1.1*1e8, 1.9*1e8)
ax1.set_xlabel('Date')
ax1.set_ylabel('Hash Rate (EH/s)')

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.plot(date_df, closePrice, color = color)
ax2.set_ylim(3300, 4700)
ax2.set_ylabel('Price (USD)')

plt.show()