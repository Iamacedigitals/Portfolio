import websocket 
import json
import pandas as pd

def on_message (ws, message):
	response = json.loads(message)
	crypto_pair = response["data"]['s']
	data =  {
		crypto_pair:{
		"Open_time":response["data"]['k']["t"],
		"Close_time":response["data"]['k']["T"],
		"open":float(response["data"]['k']["o"]),
		"high":float(response["data"]['k']["h"]),
		"low": float(response["data"]['k']["l"]),
		'close':float(response["data"]['k']["c"]),
		"Volume":response["data"]['k']["v"],
		"Volume Quote":response["data"]['k']["Q"]
	}
}
	try:
		with open("response.json", "r") as file:
			price_snapshot = json.load(file)
		if response["data"]['s'] not in price_snapshot:
			with open("response.json", "w") as f:
				price_snapshot[response["data"]['s']] ={
					"Open_time": response["data"]['k']["t"],
					"Close_time": response["data"]['k']["T"],
					"open":	float(response["data"]['k']["o"]),
					"high":	float(response["data"]['k']["h"]),
					"low":	float(response["data"]['k']["l"]),
					'close': float(response["data"]['k']["c"]),
					"Volume": response["data"]['k']["v"],
					"Volume Quote": response["data"]['k']["Q"]
				}

				json.dump(price_snapshot, f, indent= 4)
		elif response["data"]['s'] in price_snapshot:
				with open("response.json", "w") as f:
					price_snapshot[response["data"]['s']] =data[response["data"]['s']]
					json.dump(price_snapshot, f, indent= 4)							
	except:
		with open("response.json", "w") as price_snapshot:
			json.dump(data, price_snapshot, indent= 4)
	ws.close()
		
def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed connection")

def on_open(ws):
    print("Connection opened")
