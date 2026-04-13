import numpy as np
import pandas as pd
# import json
import Database as Db

class Watchlist:
	def __init__(self):
		self.Price_list = Db.pull_price_data() # get webhook data eventually.
		self.watchlist = {}
	def create_watchlist(self, name = "New List"):
		query = input(f"""
You have created {name.upper()}:

Would you like to add elements to {name.upper()}
(Y/N);
		""").lower()
		if (query == "y") | (query == "yes"):
			self.watchlist.update({
			name.upper():{}
			})
			self.add_instruments(name.upper())
			return self.watchlist
		else:
			print(f"No elements are in {name.upper()}")
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
				
				
	def remove_instruments(self):
		query = input('Enter the name of the Watchlist:>> ').upper()
		if query in self.watchlist:
			rm_instrument = input(f"""
The available instruments are: {list(self.watchlist[query].keys())}, 
Enter X to remove it:: """).upper()
			if rm_instrument in self.watchlist[query]:
				del self.watchlist[query][rm_instrument]
				print(f"{rm_instrument} Removed!!")
				print(self.watchlist[query])
				return self.watchlist[query]
			else:
				print("This instrument is not found there")
		elif query not in self.watchlist:
			print('Watchlist not found!! ')
			retry = input('Would you like to re-enter the name?? (y/n)')
			if (retry == "yes") | (retry == 'y'):
				self.remove_instruments()
				return self.watchlist
				
	def remove_watchlist(self):
		rm_watchlist = input(f"""
The available watchlists are: {list(self.watchlist.keys())},
Enter X to remove it:: """).upper()
		if rm_watchlist in self.watchlist:
			del self.watchlist[rm_watchlist]
			print(f"{rm_watchlist} Removed!!")
			print(self.watchlist)
			return self.watchlist
		elif rm_watchlist not in self.watchlist:
			print('Watchlist not found!! ')
			retry = input('Would you like to re-enter the name?? (y/n)')
			if (retry == "yes") | (retry == 'y'):
				self.remove_watchlist()
				return self.watchlist
			else:
				print('Thanks 😊😊')
				return self.watchlist