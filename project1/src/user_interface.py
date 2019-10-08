"""
This file will serve as the main user interface with the db
"""
import os
from db_helper import get_client, query_data

DATABASE = 'csci79525_proj1'

db_client = get_client()
db = db_client[DATABASE]

os.system('cls' if os.name=='nt' else 'clear')
user_input = input("Identifier:")
while user_input != "quit":

    collection_to_query = input("Collection to query:")

    res = query_data({"identifier": {'$regex': user_input}}, db[collection_to_query], 10)

    print("\n Results: \n")
    for doc in res:
        print(doc)

    input("\nPress enter to continue...")

    os.system('cls' if os.name=='nt' else 'clear')
    user_input = input("Identifier:")

os.system('cls' if os.name=='nt' else 'clear')
