from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


def get_client():
    return MongoClient('localhost', 27017)


def test_connection(client):
    try:
        info = client.server_info() # Forces a call.
        return info
    except ServerSelectionTimeoutError:
        return "Server Error"
