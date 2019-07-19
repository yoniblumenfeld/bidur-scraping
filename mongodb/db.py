import pymongo

def get_db_instance():
    return pymongo.MongoClient('mongodb://localhost:27017/')['bidurdb']

