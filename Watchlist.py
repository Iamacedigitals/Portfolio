import numpy as np
import pandas as pd
import json
import Database as Db

class Watchlist():
	def __init__(self):
		self.Price_list = Db.pull_data() # get webhook data eventually.
		self.watchlist = {}
	def create_watchlist(self, name = "New List"):
		query = input(f"""
You have created {name}:

Would you like to add elements to {name}
(Y/N);
		""").lower()
		if (query == "y") | (query == "yes"):
			self.watchlist.update({
			name:{}
			})
			self.add_instruments(name)
			return self.watchlist
		else:
			print(f"No elements are in {name}")
			print("Thanks for running this command")
			return self.watchlist
			
			
	def add_instruments(self, name):
		print(f"You can add {list(self.Price_list.keys())[0:4]}")
		query = input(f"Enter instrument to add to {name} ").upper()
		if (query not in self.Price_list):
			print(f"An error occured, {query} not in Price List")
			retry = input("Would you like to try again?? ")
			if (retry == "y") | (retry == "yes"):
				self.add_instruments(name)
			else:
				print(f"""
You created a new Watchlist with {len(self.watchlist[name])} items. 
Thanks for using 😊😊
					""")
					
		else:
			if query not in self.watchlist[name]:
				self.watchlist[name].update({
				query : self.Price_list[query]["close"]
				})
				add_more = input("would you like to add more?? (Y/N) ").lower()
				if (add_more == "y") | (add_more == "yes"):
					self.add_instruments(name)
				else:
					print(f"""
You created a new Watchlist with {len(self.watchlist[name])} items. 
Thanks for using 😊😊
					""")
				return self.watchlist
			else:
				print("This block ran")
				self.watchlist[name].update({
				query : int(self.Price_list[query]["close"])
				})
				return self.watchlist

n_watchlist = Watchlist()
print(n_watchlist.create_watchlist(name = "Black list"))