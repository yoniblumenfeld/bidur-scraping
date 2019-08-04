import pymongo

client = pymongo.MongoClient('bidurdb://localhost:27017/')
db = client['bidurdb']
db.create_collection('zappa')
