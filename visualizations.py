import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import nbformat

def graficas(df, symbol):
    # separamos el DataFrame por exchanges
    exchanges = df.exchange.unique()
    fig = make_subplots(rows=2, cols=3,
                        subplot_titles=('Level', 'ask_Volume', 'bid_Volume', 'total_vol', 'Mid_Price', 'VWAP'))

    # para cada exchange, añadimos las gráficas correspondientes
    for i, exchange in enumerate(exchanges, start=1):
        df_exchange = df[df.exchange == exchange]

        fig.add_trace(go.Scatter(x=df_exchange.timeStamp, y=df_exchange.Level, mode='lines', name=f'{exchange} Level'), row=1, col=i)
        fig.add_trace(go.Scatter(x=df_exchange.timeStamp, y=df_exchange.ask_Volume, mode='lines', name=f'{exchange} ask_Volume'), row=1, col=i)
        fig.add_trace(go.Scatter(x=df_exchange.timeStamp, y=df_exchange.bid_Volume, mode='lines', name=f'{exchange} bid_Volume'), row=1, col=i)
        fig.add_trace(go.Scatter(x=df_exchange.timeStamp, y=df_exchange.total_vol, mode='lines', name=f'{exchange} total_vol'), row=2, col=i)
        fig.add_trace(go.Scatter(x=df_exchange.timeStamp, y=df_exchange.Mid_Price, mode='lines', name=f'{exchange} Mid_Price'), row=2, col=i)
        fig.add_trace(go.Scatter(x=df_exchange.timeStamp, y=df_exchange.VWAP, mode='lines', name=f'{exchange} VWAP'), row=2, col=i)

    # actualizamos el layout y mostramos la figura
    fig.update_layout(height=600, width=1000, title_text=f'{symbol} - Order Book Data')
    fig.show()
