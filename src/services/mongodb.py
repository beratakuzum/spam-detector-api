from pymongo import MongoClient
from src.utils.errors import SDerror

import os


class MongoDbService:

    def __init__(self, db_name):
        self.mongo_client = MongoClient(os.getenv('DB_PORT_27017_TCP_ADDR'), 27017)
        self.db = self.mongo_client.get_database(db_name)
        print("ADDRESS: ", os.getenv('DB_PORT_27017_TCP_ADDR'))

    def insert_one(self, collection_name, doc):

        collection = self.db[collection_name]

        try:
            res = collection.insert_one(doc)
        except Exception as e:
            raise SDerror(
                message="Cannot Insert into DB",
                status_code=502,
                error_type="DB Insert Error"
            )

        return res

    def find_one(self, collection_name, where, select=None):
        collection = self.db[collection_name]
        try:
            res = collection.find_one(where, select)
        except Exception as e:
            raise SDerror(
                message="Cannot Find in the DB",
                status_code=502,
                error_type="DB Find Error"
            )

        return res
