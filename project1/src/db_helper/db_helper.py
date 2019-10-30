"""
Utility helper functions to insert into db.
Mostly mongo client.
TODO: Write utlilty functions for neo4j?
"""
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


def get_client():
    return MongoClient('localhost:27017')


def test_connection(client):
    try:
        info = client.server_info() # Forces a call.
        return info
    except ServerSelectionTimeoutError:
        return "Server Error"


def insert_data(data, col):
    try:
        col.insert_one(data)
    except:
        print('Insert Error')


def insert_many_data(list_data, col):
    try:
        return col.insert_many(list_data)
    except:
        print('Insert Error')


def count_documents(query, col):
    try:
        return col.count_documents(query)
    except:
        return None


def query_data_find(query, col, count=0):
    try:
        return col.find(query, {'_id': False}).limit(count)
    except:
        return None


def drop_db(db_client, db):
    try:
        db_client.drop_database(db)
    except:
        print('Drop DB Error')


# *NOTE: This is a very expensive operation. Set debug flag to False to make program run faster
def insert_progress_printer(total_lines, current_count, data_type='', print_every_n_count=1, debug=True):
    if debug and current_count % print_every_n_count == 0:
        os.system('cls' if os.name=='nt' else 'clear')
        percentage = round((current_count/total_lines) * 100 , 2)
        print(data_type + ' Progress: ' + str(percentage) + '%')
    # If debug flag is false, just print after every 100000 lines
    elif not debug and current_count % 100000 == 0:
        percentage = round((current_count/total_lines) * 100 , 2)
        print(data_type + ' Progress: ' + str(percentage) + '%')
