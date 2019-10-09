"""
This file will serve as the main user interface with the db
"""
import os
from db_helper import get_client, query_data

DATABASE = 'csci79525_proj1'

db_client = get_client()
db = db_client[DATABASE]


def print_menu(user_input):
    if user_input == "0":
        os.system('cls' if os.name=='nt' else 'clear')
        print("==== Main Menu ====")
        print("Select collection to query")
        print("1) Compound")
        print("2) Diseases")
        print("3) Genes")
        print("4) Anatomy")
        print("5) Edges")
        print("6) Quit")
    elif user_input == "1":
        os.system('cls' if os.name=='nt' else 'clear')
        print("==== Compound ====")
        print("Query by:")
    elif user_input == "2":
        os.system('cls' if os.name=='nt' else 'clear')
        print("==== Diseases ====")
    elif user_input == "3":
        os.system('cls' if os.name=='nt' else 'clear')
        print("==== Genes ====")
    elif user_input == "4":
        os.system('cls' if os.name=='nt' else 'clear')
        print("==== Anatomy ====")


def generate_query(col_type):
    if col_type == "6":
        query_string = input("edge_type query:")
        return {"edge_type": query_string}
    else:
        query_string = input("value query:")
        return {"value": query_string}


user_input = "0"
while user_input != "6":
    print_menu(user_input)
    user_input = input("\nInput(1-6):")
    print_menu(user_input)
    query = generate_query(user_input)
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
