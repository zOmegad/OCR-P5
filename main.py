import mysql.connector
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def database_setup():
	
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
		mycursor.execute("CREATE DATABASE food_database")
		mycursor.execute("USE food_database")
		mycursor.execute("CREATE TABLE category (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))") 
		mycursor.execute("CREATE TABLE food (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), nutriscore_data INT, category_id INT, FOREIGN KEY (category_id) REFERENCES category(id))") 
		mycursor.execute("INSERT INTO food (name, nutriscore_data) VALUES ('Nutella', '10')") 
		mycursor.execute("INSERT INTO category (name) VALUES ('Dessert')") 
		mydb.commit()
	
	mycursor.execute("SHOW TABLES")
	for tabl in mycursor:
		print(tabl)
		#mycursor.execute("CREATE TABLE food (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), nutriscore_data INT)") 
		#mycursor.execute("CREATE TABLE categorie (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))") 


	#mycursor.execute("DROP DATABASE food_database")

def menu():
	print("Tapez le nom d'un produit :")
	food = input()

	response = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0={}&page_size=100&json=true'.format(food))

	json_response = response.json()

	product = json_response["products"]

	for item in product:
		print("nom: " + item["product_name"])
		print("categorie: " + item["compared_to_category"])
		#print("indice gras: " + str(item["nutriscore_data"]["saturated_fat_points"]))
		print("nutriscore: " + str(item["nutriscore_data"]["score"]))
		#print("indice sucre: " + str(item["nutriscore_data"]["sugars_points"]))
		#print("indice sel: " + item["nutrient_levels"]["salt"])
		print("                ")

database_setup()