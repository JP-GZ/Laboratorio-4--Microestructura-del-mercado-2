import asyncio
import nest_asyncio
nest_asyncio.apply()
from data import orderbooks_df
import time

async def get_orderbooks(exchanges,run_time,symbol):
    data = await (orderbooks_df(exchanges=exchanges, run_time=run_time, symbol=symbol))
    return data


# exchanges = ["bitforex", "huobipro", "bitmart"]
# run_time = 10
# symbol = "ETH/BTC"
# ETH_BTC = asyncio.run(get_orderbooks(exchanges,run_time,symbol))
# print(ETH_BTC.info())
# time.sleep(5)
# symbol2 = "BTC/USDT"
# BTC_USDT = asyncio.run(get_orderbooks(exchanges,run_time,symbol2))
# print(BTC_USDT)