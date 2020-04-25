import mysql.connector
import requests
import os
from dotenv import load_dotenv
from Output import Output
load_dotenv()

class Database:

	def __init__(self):
		self.empty_database = True
		try:
			self.mydb = mysql.connector.connect(
			  host="localhost",
			  user=os.getenv("USER"),
			  passwd=os.getenv("PASSWORD"),
			  database="food_database",
			)

			self.empty_database = False
			
		except:
			self.mydb = mysql.connector.connect(
			  host="localhost",
			  user=os.getenv("USER"),
			  passwd=os.getenv("PASSWORD"),
			)
		
		self.mycursor = self.mydb.cursor()


		self.food_store = str()
		self.food_name = str()
		self.food_nutriscore = int()
		self.category_id = int()
		self.food_url = str()

	def check_database(self, my_database, my_output):
		if self.empty_database == True:
			my_database.database_setup(my_database)
		else:
			print("Base de donnée ok")
		my_output.main_menu(my_database, my_output)

	def database_category_insertion(self):
		self.mycursor.execute("USE food_database")

		sql_query = """INSERT INTO category (Name) VALUES(%s) """
		record_tuple = (self.category_name)
		self.mycursor.execute(sql_query,(record_tuple,))
		self.mydb.commit()
		print("Ajout de {}".format(self.category_name))

	def database_food_insertion(self):
		self.mycursor.execute("USE food_database")

		sql_query = """INSERT INTO food (name, nutriscore_data, category_id, store, url) VALUES(%s, %s, %s, %s, %s) """
		record_tuple = (self.food_name, self.food_nutriscore, self.category_id, self.food_store, self.food_url)
		self.mycursor.execute(sql_query, record_tuple)
		self.mydb.commit()
		print("Ajout de {}".format(self.food_name))

	def database_setup(self, my_database):
		print("Création de la base de donnée...")
		self.mycursor.execute("CREATE DATABASE food_database DEFAULT CHARACTER SET 'utf8mb4'")
		self.mycursor.execute("USE food_database")
		self.mycursor.execute("CREATE TABLE category (Id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))") 
		self.mycursor.execute("CREATE TABLE food (Id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), nutriscore_data INT, category_id INT, store TEXT(255), url VARCHAR(255), FOREIGN KEY (category_id) REFERENCES category(id))")
		self.mycursor.execute("CREATE TABLE saved_food(ID INT AUTO_INCREMENT PRIMARY KEY, food_id INT, FOREIGN KEY (food_id) REFERENCES food(id))")
		category_link = requests.get('https://fr.openfoodfacts.org/categories.json')
		json_category = category_link.json()
		product = json_category["tags"]
		for item in product[:50]:
			self.category_name = item["name"]
			my_database.database_category_insertion()


		self.mycursor.execute("SELECT * FROM category")
		categories = self.mycursor.fetchall()
		for category in categories:
			self.category_id = category[0]
			food_link = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0={}&page_size=50&json=true'.format(category[1]))
			json_food_link = food_link.json()
			item = json_food_link["products"]
			for food in item:
				if "product_name" in food:
					self.food_name = food["product_name"] 
					if "nutriscore_data" in food:
						self.food_nutriscore = food["nutriscore_data"]["score"]
					else:
						pass
					if "stores" in food:
						self.food_store = food["stores"]
					if "url" in food:		 
						self.food_url = food["url"]
					my_database.database_food_insertion()
				else:
					pass
