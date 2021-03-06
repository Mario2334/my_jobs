import pymongo


class mongoclient:
    def __init__(self, collection):
        # mongo_uri = "mongodb://:sanketm221995" + urllib.quote("Makramhetal") +
        # "@cluster0-shard-00-00-hf2ut.mongodb.net:27017,cluster0-shard-00-01-hf2ut.mongodb.net:27017,
        # cluster0-shard-00-02-hf2ut.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=Cluster0-shard-0&authSource
        # =admin"
        client = pymongo.MongoClient("mongodb+srv://jobs:opC5GYuS3XjH7oRV@myjobs-ouchy.mongodb.net/test?retryWrites=true&w=majority")
        print('connected')
        jobs_db = client['jobs']
        self.table = jobs_db[collection]

    def insert_data(self, data_dtict, ignore_check=False):
        if ignore_check:
            self.table.insert_one(data_dtict)
        else:
            if not self.check_if_data_present(data_dtict):
                self.table.insert_one(data_dtict)

    def check_if_data_present(self, data_dict):
        if not self.table.find_one({'title': data_dict['title']}):
            return False
        else:
            return True

    def check_id(self, _id):
        if not self.table.find_one({'_id': _id}):
            return False
        else:
            return True

    def mk_change(self, title, *args):
        pass
