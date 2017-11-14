import config
from pymongo import MongoClient

class Database:
    # Uncomment for local mongo database:
    #client = MongoClient()
    client = MongoClient("mongodb://{user}:{pass}@{host}/{db}".format({
        "user": config.MONGO_USERNAME,
        "pass": config.MONGO_PASSWORD,
        "host": config.MONGO_HOST,
        "db": config.MONGO_DATABSE
    }))
    
    @staticmethod
    def get_client():
        return Database.client
