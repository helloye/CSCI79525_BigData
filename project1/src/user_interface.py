"""
This file will serve as the main user interface with the db
"""
import os, re
from db_helper import get_client, query_data_find, count_documents

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


def query_compound_nodes():
    search_string = input("Enter Compound ID:")
    regx = re.compile(search_string, re.IGNORECASE)
    query = {'$or': [
        {"identifier": {'$regex': regx}},
        {"value": {'$regex': regx}}
    ]}
    count = count_documents(query, db.compounds)
    res = list(query_data_find(query, db.compounds))
    if count > 1:
        index = 1
        for doc in res:
            print(str(index) + ") " + doc['identifier'] + " - " + doc['value'])
            index += 1

        desired_index = input("\nMultiple results, select desired compound:")
        compound = res[int(desired_index) - 1]
    elif count == 1:
        compound = res[0]

    print("You have selected")
    print(compound)

    # TODO: Query the edge collection and display all associated edges with selected compound.

user_input = "0"
while user_input is not "5":
    print_menu()
    user_input = input("\nInput(1-5):")
    if user_input is not "5":
        os.system('cls' if os.name=='nt' else 'clear')
        if user_input is "1":
            query_compound_nodes()

        input("\n\nPress enter to continue...")

os.system('cls' if os.name=='nt' else 'clear')
