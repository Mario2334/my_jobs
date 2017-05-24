import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
jobs_db = client['jobs']
