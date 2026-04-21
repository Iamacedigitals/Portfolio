
import numpy as np
import websocket 
import src.data_request as dr
import json
import asyncio
assets = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", 
    "XRPUSDT", "ADAUSDT", "DOGEUSDT", 
    "SOLUSDT", "TRXUSDT", "DOTUSDT",
     
    "MATICUSDT", "LTCUSDT", "BCHUSDT", 
    "LINKUSDT", "ATOMUSDT", "AVAXUSDT",
    "UNIUSDT", "ETCUSDT", "XLMUSDT",
    
    "FILUSDT", "NEARUSDT", "APTUSDT", 
    "ARBUSDT", "OPUSDT", "SUIUSDT", 
    
    "SHIBUSDT", "PEPEUSDT", "WIFUSDT", 
    "INJUSDT", "RUNEUSDT", "AAVEUSDT",
    
    "SNXUSDT", "MKRUSDT", "COMPUSDT",
    "LDOUSDT", "ICPUSDT","VETUSDT", 
    "ALGOUSDT", "QNTUSDT", "EOSUSDT",
     
    "THETAUSDT", "GRTUSDT", "SANDUSDT", 
    "MANAUSDT", "AXSUSDT", "GALAUSDT",
    "FTMUSDT", "KAVAUSDT", "ZILUSDT", 
    
    "IOTAUSDT", "KSMUSDT",
    "FLOWUSDT", "CHZUSDT", "ENJUSDT", 
    "BLURUSDT", "ARKUSDT",
    "STXUSDT", "HBARUSDT", "XTZUSDT",
    
     "XMRUSDT", "CRVUSDT","BALUSDT", 
     "DYDXUSDT", "GMXUSDT", "PENDLEUSDT", 
     "RSRUSDT", "1INCHUSDT", "LRCUSDT", 
     
     "ZRXUSDT", "ENAUSDT", "WLDUSDT",
    "TIAUSDT", "SEIUSDT", "JUPUSDT", 
    "PYTHUSDT", "BONKUSDT", "RNDRUSDT", 
    "FETUSDT", "AGIXUSDT","OCEANUSDT",
     
    "LPTUSDT","IMXUSDT", "APEUSDT", 
    "GNOUSDT", "RPLUSDT", "MINAUSDT",
    "KDAUSDT", "CFXUSDT", "FLUXUSDT",
     
    "IOSTUSDT", "RVNUSDT","QTUMUSDT", 
    "XECUSDT", "SCUSDT", "DGBUSDT", 
    "HNTUSDT","STORJUSDT", "AUDIOUSDT", 
    "CELRUSDT", "SUSHIUSDT", "YFIUSDT"
]
assets = [asset.lower() + "@kline_1m" for asset in assets]
assets= "/".join(assets)    		

socket = f"wss://stream.binance.com:9443/stream?streams={assets}"
	
def load_price_data(ws):
	ws.on_open = dr.on_open
	ws.run_forever()
# Figure out a way to asynchronously change this element of watchlist and pull data at the same time, so that ase we are pulling data on Watchlist we can be automatically updating price. 	
		
def pull_price_data() -> dict:
	ws = websocket.WebSocketApp(
		socket, 
		on_message = dr.on_message,
		on_error= dr.on_error,
		on_close= dr.on_close
)
	load_price_data(ws)		
	with open ("response.json", "r") as response:
		print(response)
		return json.load(response)
		
def save_watchlist():
    pass