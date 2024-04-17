import os 
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

USER_DB = os.getenv("USER_DB")

db_client = MongoClient(os.getenv("DATABASE_URL")).USER_DB
