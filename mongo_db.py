import pymongo

class Mongo:
    def __init__(self, server_url, db_name, username, password):
        url_string = "mongodb+srv://"
        url_string += "{}:{}@{}".format(username, password, server_url)
        url_string += "?retryWrites=true&w=majority"
        self.__client = pymongo.MongoClient(url_string)
        self.__db = self.__client["db_name"]
    
    def get_db(self):
        return self.__db
    
    @staticmethod
    def pymongo():
        return pymongo
