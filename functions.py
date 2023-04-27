import datetime
import numpy as np
import pandas as pd


def roll_spread_df(orderbook):
    t0 = orderbook.loc[: ,"datetime"].values[0]
    td = t0 + np.timedelta64(1, "m")
    
    n = sum(orderbook["datetime"] <= td)

    pt = orderbook.loc[:, "mid_price"]
    
    effective_roll = []
    
    for i in range(2*n, len(pt)):
        pt0 = pt[i-2*n:i-n]
        pt1 = pt[i-n:i]
        effective_roll.append(2 * np.abs(np.cov(pt0, pt1)[0][1])**0.5)
    
    
    orderbook = orderbook.iloc[2*n:, :]
    orderbook["effective_spread"] = effective_roll
    return orderbook.loc[:, ["datetime", "mid_price", "spread", "effective_spread"]].set_index("datetime")
    