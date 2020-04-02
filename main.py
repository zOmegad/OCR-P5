import mysql.connector
import requests
import os
from dotenv import load_dotenv
load_dotenv()


mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv("USER"),
  passwd=os.getenv("PASSWORD")
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE food_database")

mycursor.execute("SHOW DATABASES")

print("Tapez le nom d'un produit :")
food = input()

response = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0={}&json=true'.format(food))

json_response = response.json()

product = json_response["products"]

for item in product:
	print("nom: " + item["product_name_fr"])
	print("categorie: " + item["compared_to_category"])
	print("indice gras: " + str(item["nutriscore_data"]["saturated_fat_points"]))
	print("indice sucre: " + str(item["nutriscore_data"]["sugars_points"]))
	print("indice sel: " + item["nutrient_levels"]["salt"])
	print("                ")
