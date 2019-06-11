import getpass
import pymongo

def get_mongo_connection():
    return pymongo.MongoClient()