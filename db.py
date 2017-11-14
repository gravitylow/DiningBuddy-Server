import config as app_config
from pymongo import MongoClient

class Database:
    # Uncomment for local mongo database:
    #client = MongoClient()
    client = MongoClient("mongodb://{user}:{password}@{host}/{db}".format(
        user=app_config.MONGO_USERNAME,
        password=app_config.MONGO_PASSWORD,
        host=app_config.MONGO_HOST,
        db=app_config.MONGO_DATABSE
    ))

    @staticmethod
    def get_client():
        return Database.client
