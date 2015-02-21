from pymongo import MongoClient

class Database:
    # Uncomment for local mongo database:
    #client = MongoClient()
    client = MongoClient('mongodb://flask:**REMOVED**@**REMOVED**/cnu')
    
    @staticmethod
    def get_client():
        return Database.client
