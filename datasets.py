import pymongo


class mongoclient:
    def __init__(self, collection):
        # mongo_uri = "mongodb://:sanketm221995" + urllib.quote("sohana@123") +
        # "@cluster0-shard-00-00-hf2ut.mongodb.net:27017,cluster0-shard-00-01-hf2ut.mongodb.net:27017,
        # cluster0-shard-00-02-hf2ut.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=Cluster0-shard-0&authSource
        # =admin"
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        print('connected')
        jobs_db = client['jobs']
        self.table = jobs_db[collection]

    def insert_data(self, data_dtict):
        if not self.check_if_data_present(data_dtict):
            self.table.insert_one(data_dtict)

    def check_if_data_present(self, data_dict):
        if not self.table.find_one({'title': data_dict['title']}):
            return False
        else:
            return True

    def mk_change(self, title, *args):
        pass
