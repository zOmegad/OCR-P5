import mysql.connector
from mysql.connector import Error
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def database_category_insertion(name, mydb):
	mycursor = mydb.cursor()
	mycursor.execute("USE food_database")

	sql_query = """INSERT INTO category (Name) VALUES(%s) """
	record_tuple = (name)
	mycursor.execute(sql_query,(record_tuple,))
	mydb.commit()
	print("Ajout de {}".format(name))

def database_food_insertion(food_name, food_nutriscore, category_id):
	mycursor = mydb.cursor()
	mycursor.execute("USE food_database")

	sql_query = """INSERT INTO food (name, nutriscore_data, category_id) VALUES(%s, %s, %s) """
	record_tuple = (food_name, food_nutriscore, category_id)
	mycursor.execute(sql_query, record_tuple)
	mydb.commit()
	print("Ajout de {}".format(food_name))

def database_setup():
	category_link = requests.get('https://fr.openfoodfacts.org/categories.json')
	json_category = category_link.json()
	product = json_category["tags"]
	for item in product[:50]:
		category_name = item["name"]
		database_category_insertion(category_name, mydb)


	mycursor.execute("SELECT * FROM category")
	categories = mycursor.fetchall()
	for category in categories:
		category_id = category[0]
		food_link = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0={}&page_size=100&json=true'.format(category[1]))
		json_food_link = food_link.json()
		item = json_food_link["products"]
		for food in item:
			if "product_name" in food:
				food_name = food["product_name"] 
				if "nutriscore_data" in food:
					food_nutriscore = food["nutriscore_data"]["score"]
					database_food_insertion(food_name, food_nutriscore, category_id)
				else:
					pass
			else:
				pass

try:
	mydb = mysql.connector.connect(
	  host="localhost",
	  user=os.getenv("USER"),
	  passwd=os.getenv("PASSWORD"),
	  database="food_database"
	)
	mycursor = mydb.cursor()
	mycursor.execute("USE food_database")
	
except:
	mydb = mysql.connector.connect(
	  host="localhost",
	  user=os.getenv("USER"),
	  passwd=os.getenv("PASSWORD")
	)
	mycursor = mydb.cursor()

	#mycursor.execute("DROP DATABASE food_database")
	print("Création de la base de donnée...")
	mycursor.execute("CREATE DATABASE food_database")
	mycursor.execute("USE food_database")
	mycursor.execute("CREATE TABLE category (Id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))") 
	mycursor.execute("CREATE TABLE food (Id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), nutriscore_data INT, category_id INT, FOREIGN KEY (category_id) REFERENCES category(id))") 

	database_setup()

print("Base de donnée ok")