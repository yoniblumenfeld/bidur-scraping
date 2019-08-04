import pymongo

def get_db_instance():
    return pymongo.MongoClient('bidurdb://localhost:27017/')['bidurdb']

