
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

url = "mongodb+srv://Rishabh_db:Rishabh2001@cluster0.y61xux1.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(url, server_api=ServerApi('1'))

db = client.invertory_db
user_collection = db["user_inventory"]
university_collection = db["university_inventory"]
college_collection = db["college_inventory"]
qr_collection = db["qr_inventory"]