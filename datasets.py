import pymongo


class mongoclient:
    def __init__(self):
        client = pymongo.MongoClient('mongodb://localhost:27017')
        jobs_db = client['jobs']
        self.table = jobs_db['extracted jobs']

    def insert_data(self, data_dtict):
        if not self.check_if_data_present(data_dtict):
            self.table.insert_one(data_dtict)

    def check_if_data_present(self, data_dict):
        if not self.table.find_one({'title': data_dict['title']}):
            return False
        else:
            return True
