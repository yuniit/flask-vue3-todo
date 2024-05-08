from pymongo import MongoClient
from config import Config

class Connection:
    def __new__(cls, database):
        connection = MongoClient(port=Config.port, host=Config.host)
        return connection[database]


