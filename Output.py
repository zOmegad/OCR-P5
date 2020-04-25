import os

class Output:

	def __init__(self):
		self.random_categories = "SELECT * FROM category ORDER BY RAND() LIMIT 7"
		self.food_picker_rand = "SELECT * FROM food WHERE category_id=%s ORDER BY RAND() LIMIT 10"
		self.food_picker = "SELECT * FROM food WHERE category_id=%s"
		self.selected_food = "SELECT * FROM food WHERE id=%s"
		self.food_saver = """INSERT INTO saved_food (food_id) VALUES(%s) """
		self.my_saved_food = "SELECT * FROM saved_food"

	def category_picker(self, my_database):
		my_database.mycursor.execute(self.random_categories)
		rand_cat = my_database.mycursor.fetchall()
		for x in rand_cat:
			print(str(x[0]) + "  " + str(x[1]))

	def food_list_from_cat(self, my_database, choice_cat):
		my_database.mycursor.execute(self.food_picker_rand,(choice_cat,))
		rand_products = my_database.mycursor.fetchall()
		for x in rand_products:
			print(str(x[0]) + "  " + str(x[1]) + " | nutriscore: " + str(x[2]))

	def healthy_food(self, my_database, food_choice, choice_cat):
		my_database.mycursor.execute(self.selected_food, (food_choice,))
		product = my_database.mycursor.fetchall()
		for x in product:
			product_nutriscore = x[2]

		my_database.mycursor.execute(self.food_picker, (choice_cat,))
		all_products = my_database.mycursor.fetchall()
		healthier_food = None
		for x in all_products:
			if x[2] < product_nutriscore:
				healthier_food = x
			else:
				pass
		print("We've found :")
		print(str(healthier_food[1]))
		print("Nutriscore : " + str(healthier_food[2]))
		print("Store: " + str(healthier_food[4]))
		print("Link : " + str(healthier_food[5]))

	def save_food(self, my_database, food_choice):
		my_database.mycursor.execute(self.food_saver, (food_choice,))
		my_database.mydb.commit()
		print("Product saved.")

	def my_food(self, my_database, my_output):
		my_database.mycursor.execute(self.my_saved_food)
		foods = my_database.mycursor.fetchall()
		for x in foods:
			my_database.mycursor.execute(self.selected_food, (x[0],))
			food = my_database.mycursor.fetchall()
			for y in food:
				print("--------------")
				print(y[1])
				print(y[5])
		my_output.exit_program(my_database, my_output)

	def exit_program(self, my_database, my_output):
		while True:
			try:
				print(" ")
				choice = str(input("Press 'b' to back, 'q' to quit"))
				if choice == "b":					
					my_output.main_menu(my_database, my_output)
					break
				elif choice == "q":
					break
				else:
					print("I didn't understand your choice")
					pass
			except:
				print("Please type a letter")

	def main_menu(self, my_database, my_output):
		os.system('cls' if os.name == 'nt' else 'clear') # clear terminal

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
		print("1. Show categories")
		print("2. My saved products")
		

		choice_1 = int(input())
		if choice_1 == 1:
			print(" ")
			my_output.category_picker(my_database)
			while True:
				try:
					print(" ")
					choice_cat = int(input("Select a category by typing the id: "))
					break
				except ValueError:
				    print("Please enter a number.")
			print(" ")
			my_output.food_list_from_cat(my_database, choice_cat)

			while True:
				try:
					print(" ")
					food_choice = int(input("Select a product by typing the id: "))
					break
				except ValueError:
					print("Please enter a number.")
			my_output.healthy_food(my_database, food_choice, choice_cat)

			while True:
				print(" ")
				save_choice = input("Would you like to save this product ? y/n: ")
				if save_choice == "y":
					my_output.save_food(my_database, food_choice)
					break
				elif save_choice == "n": 
					break
				else:
					pass
			my_output.exit_program(my_database, my_output)
		
		elif choice_1 == 2:
			my_output.my_food(my_database, my_output)
		else:
			print("I din't understand")
		