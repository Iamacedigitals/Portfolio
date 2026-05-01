import json
from pathlib import Path
import requests
from fastapi import Depends


p = Path.cwd()
sp = p / 'src' / 'crypto_module' / 'response.json'


def read_json():
    with open(sp, "r") as data:
        crypto_data = json.load(data)

        print(json.dumps(crypto_data, indent=4))
        return crypto_data

def data_to_db():
    data = read_json()

    for crypto_pair, crypto_info in data.items():
        volume_value = None
        
        if "Volume" in crypto_info:
            volume_value = crypto_info["Volume"]
        else:
            for key in crypto_info.keys():
                if key.startswith("Volume") and key != "Volume Quote":
                    volume_value = crypto_info[key]
                    break
        
        if volume_value is None:
            print(f"Warning: No volume found for {crypto_pair}, skipping...")
            continue
        
        payload = {
            "crypto_pair": crypto_pair,
            "Open_time": crypto_info["Open_time"],
            "Close_time": crypto_info["Close_time"],
            "open_": crypto_info["open"],
            "high": crypto_info["high"],
            "low": crypto_info["low"],
            "close": crypto_info["close"],
            "Volume": volume_value,
            "Volume_Quote": crypto_info["Volume Quote"]
        }

        try:
            response = requests.post("http://localhost:8000/init db/init_db", json=payload)
            print(f"{crypto_pair}: {response.status_code}")
        except Exception as e:
            print(f"Error sending {crypto_pair}: {e}")

data_to_db()


