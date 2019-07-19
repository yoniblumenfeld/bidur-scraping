import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['bidurdb']
db.create_collection('zappa')
