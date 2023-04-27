import asyncio
import nest_asyncio
nest_asyncio.apply()
import ccxt.async_support as ccxta
import time
import pandas as pd
import numpy as pd

async def async_client(exchange_id, run_time: int, symbol: str):
    orderbook = None
    exchange = getattr(ccxta, exchange_id)()
    time_1 = time.time()
    time_f = 0
    ob = []
    while time_f <= run_time:
        print(f"Time {time_f} / {run_time}")
        try:
            await exchange.load_markets()
            market = exchange.market(symbol)
            orderbook = await exchange.fetch_order_book(market["symbol"])
            datetime = exchange.iso8601(exchange.milliseconds())
            # Unpack values
            bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
            ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
            spread = np.round(ask - bid, 10)
            # OHLC
            ohlc = await exchange.fetch_ohlcv(symbol=symbol, timeframe='1m', limit=1)

            # VWAP calculation
            bids = orderbook["bids"]
            asks = orderbook["asks"]
            x = bids + asks
            xx = [row[0] for row in x]
            yy = [row[1] for row in x]
            vwap = sum([x * y for x, y in zip(xx, yy)]) / sum(yy)

            ask_volume = sum([row[1] for row in orderbook["asks"]])
            bid_volume = sum([row[1] for row in orderbook["bids"]])
            total_vol = ask_volume + bid_volume
            # Final data format for the results
            ob.append(
                {
                    "exchange": exchange_id,
                    "timeStamp": datetime,
                    "Level": len(orderbook['asks']),
                    "ask_Volume": ask_volume,
                    "bid_Volume": bid_volume,
                    "total_vol" : total_vol,
                    "Mid_Price": (ohlc[0][2] + ohlc[0][3]) / 2,
                    "VWAP": vwap,
                    "Close_Price": ohlc[0][4],
                    "spread" : spread,
                }
            )
            # with open(r"files\archivo.txt", "w") as archivo:
            #     entrada = input(ob)
            #     if entrada.lower() == "salir":
            #         break
            #     archivo.write(entrada + "\n")
            # End time
            time.sleep(.5)
            time_2 = time.time()
            time_f = round(time_2 - time_1, 4)
        except Exception as e:
            time_2 = time.time()
            time_f = round(time_2 - time_1, 4)
            print(type(e)._name_, str(e))
    await exchange.close()
    return ob


async def multi_orderbooks(exchanges, run_time: int, symbol: str):
    input_coroutines = [
        async_client(exchange, run_time, symbol) for exchange in exchanges
    ]
    orderbooks = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return orderbooks


async def orderbooks_df (exchanges:list,run_time:int,symbol:str): # json:bool
    data = asyncio.run(multi_orderbooks(exchanges, run_time=run_time, symbol=symbol))
    data = [item for sublist in data for item in sublist]
    data = pd.DataFrame(data)
    data.set_index('exchange', inplace=True)
    return data