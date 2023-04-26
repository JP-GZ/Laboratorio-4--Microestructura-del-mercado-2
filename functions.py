import datetime
import numpy as np
import pandas as pd


def roll_spread_df(orderbook):  # Puede cambiar 
    orderbook = orderbook.reset_index()
    
    t1 = orderbook.loc[:, "timestamp"].values[-1]
    t0 = t1 - datetime.timedelta(seconds=60)
    n = sum(orderbook["timestamp"] <= t0)
    window = len(orderbook) - n

    pt1 = orderbook.loc[:, "close"]
    
    effective_roll = []
    
    for i in range(len(pt1)):
        effective_roll.append(np.abs(np.cov(pt1[i:window + i], pt1[window+i:window*2+i]))**0.5)
    
    orderbook = orderbook.iloc[n:, :]
    orderbook["effective spread"] = effective_roll
    return orderbook.loc[:, ["close", "spread", "effective spread"]]  # Puede cambiar dependiendo el nombre la columna
    


orderbook_df = pd.read_json("...")  # Pendiente por datos
