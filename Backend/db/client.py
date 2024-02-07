import os 
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

user_db = os.getenv("USER_DB")

db_client = MongoClient(os.getenv("DATABASE_URL")).user_db
