"""
This file will serve as the main user interface with the db
"""
import os
from db_helper import get_client, query_data

COL_NAME = ["db.compounds", "db.diseases", "db.anatomy", "db.genes"]

DATABASE = 'csci79525_proj1'

db_client = get_client()
db = db_client[DATABASE]


def print_menu():
    os.system('cls' if os.name=='nt' else 'clear')
    print("==== Main Menu ====")
    print("Select collection to query")
    print("1) Compound")
    print("2) Diseases")
    print("3) Anatomy")
    print("4) Genes")
    print("5) Quit")


# Query all associated data with the particular ID
def generate_query(col_type):
    return ""


user_input = "0"
while user_input is not "5":
    print_menu()
    user_input = input("\nInput(1-5):")
    if user_input is not "5":
        os.system('cls' if os.name=='nt' else 'clear')
        print("Querying: " + COL_NAME[int(user_input) - 1])
        query = generate_query(user_input)
        test = input("Press enter to continue...")
    # TODO: Query DB with example from below

os.system('cls' if os.name=='nt' else 'clear')


# os.system('cls' if os.name=='nt' else 'clear')
# user_input = input("Identifier:")
# while user_input != "5":
#
#     field_to_query = input("Field to query:")
#     collection_to_query = input("Collection to query:")
#
#     res = query_data({field_to_query: {'$regex': user_input}}, db[collection_to_query], 10)
#
#     print("\n Results: \n")
#     for doc in res:
#         print(doc)
#
#     input("\nPress enter to continue...")
#
#     os.system('cls' if os.name=='nt' else 'clear')
#     user_input = input("Identifier:")
#
# os.system('cls' if os.name=='nt' else 'clear')
