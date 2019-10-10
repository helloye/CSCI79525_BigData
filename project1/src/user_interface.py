"""
This file will serve as the main user interface with the db
"""
import os, re
from db_helper import get_client, query_data_find, count_documents

DATABASE = 'csci79525_proj1'

db_client = get_client()
db = db_client[DATABASE]


def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')


def print_menu():
    clear_screen()
    print("==== Main Menu ====")
    print("Select collection to query")
    print("1) Compound")
    print("2) Diseases")
    print("3) Anatomy")
    print("4) Genes")
    print("5) Quit")


def print_associated_results(res):
    print("\t" + res['identifier'] + " - " + res['value'])


def query_associated_data(res, edge_type, col, target_or_source = 'target_id'):
    associated_ids = []
    for r in res:
        if r['edge_type'] == edge_type:
            associated_ids.append(r[target_or_source])
    
    if len(associated_ids) == 0:
        return []

    query = {"identifier": { '$in': associated_ids}}
    return list(query_data_find(query, col))


def query_edges(s_id):
    query_string = {'$or': [{"source_id": s_id}, {"target_id": s_id}]}
    return list(query_data_find(query_string, db.edges))

'''
COMPOUND COLLECTION QUERY FUNCTION
'''
def query_compound_nodes():
    search_string = input("Enter a compound to query(ID/value):")
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
    else:
        print("\nNo results found for query: '" + search_string + "'")
        return

    print("\nYou have selected:")
    print(compound)
    input("\nPress enter to query associated data with this compound...")
    clear_screen()
    print("Querying...")
    edge_res = query_edges(compound['identifier'])

    # Self
    CrC = query_associated_data(edge_res, 'CrC', db.compounds)

    # Outgoing Edges
    CtD = query_associated_data(edge_res, 'CtD', db.diseases)
    CpD = query_associated_data(edge_res, 'CpD', db.diseases)
    CuG = query_associated_data(edge_res, 'CuG', db.genes)
    CdG = query_associated_data(edge_res, 'CdG', db.genes)
    CbG = query_associated_data(edge_res, 'CbG', db.genes)

    clear_screen()
    # Printing results
    print("==== " + compound['identifier'] + " ====")
    print("Name: " + compound['value'])
    print("==== Self Edge ====")
    print("Resembles (CrC):")
    for resembling_compound in CrC:
        print_associated_results(resembling_compound)
    print("==== Outgoing Edge ====")
    print("Treats Diseases (CtD):")
    for treates in CtD:
        print_associated_results(treates)
    print("Palliates Diseases (CtD):")
    for palliates in CpD:
        print_associated_results(palliates)
    print("Upregulates Gene (CuG):")
    for upreg in CuG:
        print_associated_results(upreg)
    print("Downregulates Gene (CdG):")
    for downreg in CdG:
        print_associated_results(downreg)
    print("Binds Gene (CbG):")
    for binds in CbG:
        print_associated_results(binds)
    print("==== Incoming Edge ====")
    print("*NONE*")


'''
DISEASES COLLECTION QUERY FUNCTION
'''
def query_disease_nodes():
    search_string = input("Enter a disease to query(ID/value):")
    regx = re.compile(search_string, re.IGNORECASE)
    query = {'$or': [
        {"identifier": {'$regex': regx}},
        {"value": {'$regex': regx}}
    ]}
    count = count_documents(query, db.diseases)
    res = list(query_data_find(query, db.diseases))
    if count > 1:
        index = 1
        for doc in res:
            print(str(index) + ") " + doc['identifier'] + " - " + doc['value'])
            index += 1

        desired_index = input("\nMultiple results, select desired disease:")
        disease = res[int(desired_index) - 1]
    elif count == 1:
        disease = res[0]
    else:
        print("\nNo results found for query: '" + search_string + "'")
        return

    print("\nYou have selected:")
    print(disease)
    input("\nPress enter to query associated data with this disease...")
    clear_screen()
    print("Querying...")
    edge_res = query_edges(disease['identifier'])

    # Self
    DrD = query_associated_data(edge_res, 'DrD', db.diseases)

    # Outgoing Edges
    DlA = query_associated_data(edge_res, 'DlA', db.anatomy)
    DuG = query_associated_data(edge_res, 'DuG', db.genes)
    DdG = query_associated_data(edge_res, 'DdG', db.genes)
    DaG = query_associated_data(edge_res, 'DaG', db.genes)

    # Incoming Edges
    CtD = query_associated_data(edge_res, 'CtD', db.compounds, 'source_id')
    CpD = query_associated_data(edge_res, 'CpD', db.compounds, 'source_id')

    clear_screen()
    # Printing results
    print("==== " + disease['identifier'] + " ====")
    print("Name: " + disease['value'])
    print("==== Self Edge ====")
    print("Resembles (CrC):")
    for resembling_diseases in DrD:
        print_associated_results(resembling_diseases)
    print("==== Outgoing Edge ====")
    print("Localizes Anatomy (DlA):")
    for localizes in DlA:
        print_associated_results(localizes)
    print("Upregulates Gene (DuG):")
    for upreg in DuG:
        print_associated_results(upreg)
    print("Downregulates Gene (DdG):")
    for downreg in DdG:
        print_associated_results(downreg)
    print("Associated with Gene (DaG):")
    for assoc in DaG:
        print_associated_results(assoc)
    print("==== Incoming Edge ====")
    print("Treated by Compound (CtD):")
    for treated_by in CtD:
        print_associated_results(treated_by)
    print("Palliated by Compound (CpD):")
    for palliated_by in CpD:
        print_associated_results(palliated_by)


'''
ANATOMY COLLECTION QUERY FUNCTION
'''
def query_anatomy_nodes():
    search_string = input("Enter an anatomy to query(ID/value):")
    regx = re.compile(search_string, re.IGNORECASE)
    query = {'$or': [
        {"identifier": {'$regex': regx}},
        {"value": {'$regex': regx}}
    ]}
    count = count_documents(query, db.anatomy)
    res = list(query_data_find(query, db.anatomy))
    if count > 1:
        index = 1
        for doc in res:
            print(str(index) + ") " + doc['identifier'] + " - " + doc['value'])
            index += 1

        desired_index = input("\nMultiple results, select desired anatomy:")
        anatomy = res[int(desired_index) - 1]
    elif count == 1:
        anatomy = res[0]
    else:
        print("\nNo results found for query: '" + search_string + "'")
        return

    print("\nYou have selected:")
    print(anatomy)
    input("\nPress enter to query associated data with this anatomy...")
    clear_screen()
    print("Querying...")
    edge_res = query_edges(anatomy['identifier'])

    # Outgoing Edges
    AuG = query_associated_data(edge_res, 'AuG', db.genes)
    AdG = query_associated_data(edge_res, 'AdG', db.genes)
    AeG = query_associated_data(edge_res, 'AeG', db.genes)

    # Incoming Edges
    DlA = query_associated_data(edge_res, 'DlA', db.diseases, 'source_id')

    clear_screen()
    # Printing results
    print("==== " + anatomy['identifier'] + " ====")
    print("Name: " + anatomy['value'])
    print("==== Self Edge ====")
    print("*NONE")
    print("==== Outgoing Edge ====")
    print("Upregulates Gene (AuG):")
    for upreg in AuG:
        print_associated_results(upreg)
    print("Downregulates Gene (AdG):")
    for downreg in AdG:
        print_associated_results(downreg)
    print("Expresses Gene (AeG):")
    for express in AeG:
        print_associated_results(express)
    print("==== Incoming Edge ====")
    print("Localized by Diseases (DlA):")
    for localized_by in DlA:
        print_associated_results(localized_by)


'''
MAIN PROGRAM LOOP
- Prints main menu
- Calls collection query function based on user selection
'''

user_input = "0"
while user_input is not "5":
    print_menu()
    user_input = input("\nInput(1-5):")
    if user_input is not "5":
        os.system('cls' if os.name=='nt' else 'clear')
        if user_input is "1":
            query_compound_nodes()
        elif user_input is "2":
            query_disease_nodes()
        elif user_input is "3":
            query_anatomy_nodes()

        input("\n\nPress enter to continue...")

clear_screen()
