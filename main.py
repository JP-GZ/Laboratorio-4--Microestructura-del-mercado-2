import asyncio
# import nest_asyncio
# nest_asyncio.apply()
from data import multi_orderbooks
import time
import pandas as pd

def get_orderbooks(exchanges,run_time,symbol):
    data = asyncio.run(multi_orderbooks(exchanges=exchanges, run_time=run_time, symbol=symbol))
    data = [item for sublist in data for item in sublist]
    data = pd.DataFrame(data)
    data.set_index('exchange', inplace=True)
    return data


# exchanges = ["bitforex", "huobipro", "bitmart"]
# run_time = 30
# symbol = "ETH/BTC"
# ETH_BTC = (get_orderbooks(exchanges,run_time,symbol))
# #ETH_BTC.to_csv(r'files\orderbooks_25abr2023.csv')
# print(ETH_BTC)
# # time.sleep(5)
# symbol2 = "BTC/USDT"
# BTC_USDT = asyncio.run(get_orderbooks(exchanges,run_time,symbofl2))
# print(BTC_USDT)
#BTC_USDT.to_csv(r'files\orderbooks_25abr2023_BTC_USDT.csv')