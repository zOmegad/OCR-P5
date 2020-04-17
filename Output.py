import os

class Output:

	def __init__(self):
		self.random_categories = "SELECT * FROM category ORDER BY RAND() LIMIT 7"
		self.food_picker = "SELECT * FROM food WHERE category_id=%s ORDER BY RAND() LIMIT 10"
		self.food_list = {}

	def category_picker(self, my_database):
		my_database.mycursor.execute(self.random_categories)
		rand_cat = my_database.mycursor.fetchall()
		for x in rand_cat:
			print(str(x[0]) + "  " + x[1])

	def food_list_from_cat(self, my_database, choice_cat):
		my_database.mycursor.execute(self.food_picker,(choice_cat,))
		rand_products = my_database.mycursor.fetchall()
		for x in rand_products:
			print(str(x[0]) + "  " + x[1])

	def main_menu(self, my_database, my_output):
		os.system('cls' if os.name == 'nt' else 'clear')

		print("#####################################################")
		print("#   ____                     ______              _  #")
		print("#  / __ \                   |  ____|            | | #")
		print("# | |  | |_ __   ___ _ __   | |__ ___   ___   __| | #")
		print("# | |  | | '_ \ / _ \ '_ \  |  __/ _ \ / _ \ / _` | #")
		print("# | |__| | |_) |  __/ | | | | | | (_) | (_) | (_| | #")
		print("#  \____/| .__/ \___|_| |_| |_|  \___/ \___/ \__,_| #")
		print("#        | |                                        #")
		print("#        |_|                                        #")
		print("#                                                   #")
		print("#####################################################")
		print(" ")
		print(" ")
		print("1. Afficher des catégories")
		print("2. Effectuer une recherche")
		

		choice_1 = int(input())
		if choice_1 == 1:
			print(" ")
			print("Selectionnez une catégorie")
			my_output.category_picker(my_database)
			choice_cat = int(input())
			print(" ")
			my_output.food_list_from_cat(my_database, choice_cat)

		elif choice_1 == 2:
			print("le 2")
		else:
			print("Tapez un chiffre du tableau bordel")
		