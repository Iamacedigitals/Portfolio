import numpy as np
import pandas as pd 
import json
from datetime import datetime

def get_init_balance():
    try:
        with open("Balance_Data.json", "r") as balance:
            balance_data = json.load(balance)
            keys = list(balance_data.keys())
            last_key = list(balance_data[keys[-1]].keys())[-1]
            current_balance = balance_data[keys[-1]][last_key]
        return current_balance["Balance"]
    except:
        with open("Balance_Data.json", "w") as balance:
            json.dump({}, balance, indent = 4)
            return 0
            
            
            
class Balance:    
	def __init__(self):
		self.Balance = get_init_balance()
		self.floating = 0 #shows the total unclosed pnl + current balance
		self.margin = 0
		self.Balance_data = {}
		
		
	def deposit_funds(self):
		query = float(input("How much do you want to deposit??: ")) # To access paymemt gateways an access binance account to deposit into with binance API 
		#Authenticate payment here 
		self.Balance += query
		self.update_balance_info(amount= query)
		return self.Balance
		
		
	def withdraw_funds(self):
		query = float(input("How much do you want to Withdraw??: "))
		if query > self.Balance:
			print("Error, Not enough funds ")
			retry = input("Retry?(y/n): ").lower()
			if (retry == "yes") | (retry == 'y'):
				self.withdraw_funds()
				self.update_balance_info(
					action="Withdrawal",
					amount= query
					)
				return self.Balance
			else:
				self.update_balance_info(amount= 0)
				pass
		elif (query<=self.Balance) & (query > 0):
			self.Balance -= query
			self.update_balance_info(
					action="Withdrawal",
					amount= query
					)
			return self.Balance
		else:
			print('An error occured')
			self.withdraw_funds()
			self.update_balance_info(
				action="Withdrawal",
				amount= query
			)
			return self.Balance
			
			
	def update_balance_info(self,amount:float, action = "deposit"):
		now = datetime.now()	
		try:
			with open("Balance_Data.json", "r") as balance:
				balance_data = json.load(balance)
				if now.strftime("%Y-%m-%d") not in balance_data:
					with open("Balance_Data.json", "w") as new_data:
						balance_data[now.strftime("%Y-%m-%d")] = {
							now.strftime("%H:%M:%S"):{ # Contains Metadata on time
							"Balance": self.Balance,
							"Amount": amount,
							"Available Margin": self.margin,
							"Action" : "Deposit" if action == "deposit" else action
						}
					}
						json.dump(balance_data, new_data, indent = 4)
					return True
				elif now.strftime("%H:%M:%S") not in balance_data[now.strftime("%Y-%m-%d")]:
					with open("Balance_Data.json", "w") as new_data:
						balance_data[now.strftime("%Y-%m-%d")][now.strftime("%H:%M:%S")]= { 
							# Contains Metadata on time
							"Balance": self.Balance, 
							"Amount": amount,
							"Available Margin": self.margin,
							"Action" : "Deposit" if action == "deposit" else action
						}
						json.dump(balance_data, new_data, indent = 4)
					return True
					
		except FileNotFoundError:
			self.Balance = 0
			with open("Balance_Data.json", "w") as balance:
				json.dump(self.Balance_data, balance, indent=4)
				
				
	def get_balance(self):
		with open("Balance_Data.json", "r") as balance:
			balance_data = json.load(balance)
			if len(balance_data) > 0:
				keys = list(balance_data.keys())
				last_key = list(balance_data[keys[-1]].keys())[-1]
				current_balance = balance_data[keys[-1]][last_key]
				return current_balance
			elif len(balance_data) == 0:
				current_balance = {"Balance": 0, "Margin":0}
				return current_balance