import Balance 
import numpy as np
import pandas as pd
import Database as db
from Balance import Balance
from Watchlist import Watchlist
import datetime
import json

class Position(Balance, Watchlist):
	now = datetime.datetime.now()
	current_date =  now.strftime("%Y-%m-%d")
	current_time = now.strftime("%H:%M:%S")

	def __init__(self):
		Balance.__init__(self)
		Watchlist.__init__(self)
		self.investment_amount = 0
		self.Holdings = {}
		self.entry_price = {}
		self.exit_price = {}
		self.leverage = {} # Asset name: Amount of leverage
		self.pnl = {} # Asset name: amount of leverage
		self.current_price = {} #Asset name: current price

	def add_position(self):
		instrument  = input(f"You can open {list(self.Price_list.keys())[0:4]}").upper()
		with open("Position.json", "w") as new_position:
				json.dump({}, new_position, indent=4)
		try:
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

					with open("Position.json", "r") as open_positions:
						positions = json.load(open_positions)
						if instrument not in positions:
							with open("Position.json", "w") as new_positions: 
								positions[instrument] = {
									"Date": self.current_date,
									"Entry Time": self.current_time, 
									"Entry": self.Price_list[instrument]["close"],
									"Holdings": holdings,
									"Leverage": leverage,
									"Investment_Margin": investment_margin,
									"Margin" : available_margin
								}
								json.dump(positions , new_positions, indent=4)
					
					more_positions = input("Would You like to add more positions: ")
					if more_positions in ["yes",  "y"]:
						self.add_position()
					else:
						print("Done, You can now check the positions in the menu: ")


				elif investment_margin > self.Balance:
					print("INSUFFICIENT FUNDS")
					deposit = input("Deposit??: ").lower()

					if deposit in ["yes",  "y"]:
						self.deposit_funds()
						self.add_position()
					else:
						print("Thanks")

			else:
				print("Instument not found: Enter a valid one: >> ")
				self.add_position()
		except FileNotFoundError:
			with open("Position.json", "w") as new_position:
				json.dump({}, new_position, indent=4)

	def check_positions(self):
		try:
			with open("Position.json", "r") as open_positions:
				positions = json.load(open_positions)
			print(pd.DataFrame(positions))
		except FileNotFoundError:
			print("No records found")
new_position = Position()

new_position.check_positions()
new_position.add_position()