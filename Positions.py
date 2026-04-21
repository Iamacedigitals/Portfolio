import Balance 
import numpy as np
import pandas as pd
import Database as db
from Balance import Balance
from Watchlist import Watchlist
import datetime
import json


class Position(Balance, Watchlist):
	def __init__(self):
		Balance.__init__(self)
		Watchlist.__init__(self)
		self.current_date = str()
		self.current_time = str()
		self.investment_amount = 0
		self.Holdings = {}
		self.entry_price = {}
		self.exit_price = {}
		self.leverage = {} # Asset name: Amount of leverage
		self.pnl = {} # Asset name: amount of leverage
		self.current_price = {} #Asset name: current price

	def price_snapshot(self,instrument_name:str, entry:int, exit=0, current=0)  ->  dict:
		file_name = "Price_snapshot.json"
		try:
			with open(file_name, 'r') as position:
				position_data = json.load(position)
				available_open_positions = [open_instruments for open_instruments in position_data]
				if instrument_name not in position_data:

					with open(file_name , "w") as new_data:
						position_data[instrument_name] = {
							"Entry_Price": [entry],
							"Exit_Price": exit,
							"Current_Price":current
						}

						json.dump(position_data, new_data, indent= 4)
				elif position_data[instrument_name]["Current_Price"] == 0:
					position_data[instrument_name]["Current_Price"] = self.Price_list[instrument_name]["close"]
				elif  position_data[instrument_name]["Exit_Price"] == 0:
					position_data[instrument_name]["Exit_Price"] = self.Price_list[instrument_name]['close']
		except FileNotFoundError:
			with open (file_name, "w") as new_snapshot:
				json.dump({}, new_snapshot, indent= 4)
			self.price_snapshot(instrument_name, entry)

	def update_snapshot(self):
		pass

	def add_position(self):
		now = datetime.datetime.now()
		self.current_date = now.strftime("%Y-%m-%d")
		self.current_time = now.strftime("%H-%M-%S")
		try:
			# Ensures the value is catched before the query so that its sychronous with the balance data 
			with open("Position.json", "r") as open_positions:
				instrument  = input(f"You can open {list(self.Price_list.keys())[0:4]}").upper()
				positions = json.load(open_positions)
				if instrument not in positions:
					if instrument in self.Price_list:
						holdings = float(input(f"How many {instrument} do you want to buy: "))
						price = self.Price_list[instrument]['close']
						leverage =float(input("Leverage: "))
						investment_margin = (price * holdings)  / leverage

						if investment_margin <= self.Balance:
							available_margin = self.Balance - investment_margin
							self.Balance -= investment_margin
							self.margin = available_margin
							self.update_balance_info(amount= investment_margin, action="Open_posiition")

							#Ensures the Entry price snapshot is created 
							self.price_snapshot(instrument, price)

							if instrument not in positions:
								with open("Position.json", "w") as new_positions: 
									positions[instrument] = {
										"Date": self.current_date,
										"Entry Time": self.current_time, 
										"Entry Price": self.Price_list[instrument]["close"],
										"Holdings": holdings,
										"Leverage": leverage,
										"Investment_Margin": investment_margin,
										"Available Margin" : available_margin
									}
									json.dump(positions , new_positions, indent=4)

							# Takes account of the current price ||| Issue here , Issue Here , Issue here
							# self.price_snapshot(instrument, price)

							# Tries to add more positions
							more_positions = input("Would You like to add more positions: ")

							if more_positions in ["yes",  "y"]:
								self.add_position()
							else:
								print("Done, You can now check the positions in the menu: ")

						elif investment_margin > self.Balance:
							print("INSUFFICIENT FUNDS")
							deposit = input("Deposit??: ").lower()
							# Tries to deposit
							if deposit in ["yes",  "y"]:
								self.deposit_funds()
								self.add_position()
							else:
								print("Thanks")
					else:
						print("Instument not found: Enter a valid one: >> ")
						self.add_position()
				else:
					holdings = float(input(f"How many {instrument} do you want to buy: "))
					price = self.Price_list[instrument]['close']
					leverage =float(input("Leverage: "))
					investment_margin = (price * holdings)  / leverage

					if investment_margin <= self.Balance:
							available_margin = self.Balance - investment_margin
							self.Balance -= investment_margin
							self.margin = available_margin
							self.update_balance_info(amount= investment_margin, action="Open_posiition")

					self.modify_positions(instrument=instrument, holdings=holdings, investment_margin=investment_margin)

					more_positions = input("Would You like to add more positions: ")

					if more_positions in ["yes",  "y"]:
						self.add_position()
					else:
						print("Done, You can now check the positions in the menu: ")

		except FileNotFoundError:
			with open("Position.json", "w") as new_position:
				json.dump({}, new_position, indent=4)
			self.add_position()

	def modify_positions(self, instrument, holdings, investment_margin):
		with open("Position.json", "r") as available_positions :
			positions = json.load(available_positions)

			if instrument in positions:

				def aggregate_price(sumArr):
						prices = np.array(sumArr)
						aggregate = np.mean(prices)
						return aggregate
				
				with open("Positions.json", "w") as update_data:
				## Note that the entry price needs an aggregation function that helps us to know the aggregate price of an asset if we have multiple positions, 
				# the entry prices should be stored in price snapshots and then calculated using the appropriate aggregation functions
				# reverse the idea of appending the prices into the open postions,instead try and update the current entry price with new price that has been aggregated from the price snapshot 
					positions[instrument]["Entry Price"] = self.Price_list[instrument]["close"]
					positions[instrument]["Available Margin"] = self.Balance
					with open('Price_snapshot.json', "r") as read_current_snapshot:
						current_snapshots = json.load(read_current_snapshot)
						if instrument in current_snapshots:
							with open("Price_snapshot", "w") as  update_snapshots:
								current_snapshots[instrument]["Entry_Price"].append(self.Price_list[instrument]["close"])
								positions[instrument]["Aggregate"] = aggregate_price(current_snapshots[instrument]["Entry_Price"])
								json.dump(current_snapshots, update_snapshots, indent=4)
						else:
							pass
					
					positions[instrument]["Holdings"] += holdings
					positions[instrument]["Investment_Margin"] += investment_margin

					json.dump(positions, update_data, indent=4)
			else:
				self.add_position()
		
	def close_positions():
		pass
	def check_positions(self):
		try:
			with open("Position.json", "r") as open_positions:
				positions = json.load(open_positions)
			print(pd.DataFrame(positions).T)
		except FileNotFoundError:
			print("No records found")
new_position = Position()
new_position.add_position()
new_position.check_positions()