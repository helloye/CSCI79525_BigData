"""
This file will serve as the main user interface with the db
"""
import os, re, sys
sys.path.append('./db_helper/')
from db_helper import get_client, query_data_find, count_documents, n4j_compound_disease

DATABASE = 'csci79525_proj1'

db_client = get_client()
db = db_client[DATABASE]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_menu():
    clear_screen()
    print("==== Main Menu ====")
    print("Select collection to query")
    print("1) Compound")
    print("2) Diseases")
    print("3) Anatomy")
    print("4) Genes")
    print("5) Find missing Compound<->Disease Edges")
    print("6) Quit")


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

        desired_index = None
        while desired_index is None:
            desired_index = input("\nMultiple results, select desired compound[1-"+str(count)+"]:")
            if not desired_index.isdigit() or int(desired_index)<1 or int(desired_index)>count:
                print("Please enter # for one of the results above...")
                desired_index = None

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

        desired_index = None
        while desired_index is None:
            desired_index = input("\nMultiple results, select desired disease[1-"+str(count)+"]:")
            if not desired_index.isdigit() or int(desired_index)<1 or int(desired_index)>count:
                print("Please enter # for one of the results above...")
                desired_index = None

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
    print("Resembles (DrD):")
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

        desired_index = None
        while desired_index is None:
            desired_index = input("\nMultiple results, select desired anatomy[1-"+str(count)+"]:")
            if not desired_index.isdigit() or int(desired_index)<1 or int(desired_index)>count:
                print("Please enter # for one of the results above...")
                desired_index = None

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
GENES COLLECTION QUERY FUNCTION
'''
def query_gene_nodes():
    search_string = input("Enter a gene to query(ID/value):")
    regx = re.compile(search_string, re.IGNORECASE)
    query = {'$or': [
        {"identifier": {'$regex': regx}},
        {"value": {'$regex': regx}}
    ]}
    count = count_documents(query, db.genes)
    res = list(query_data_find(query, db.genes))
    if count > 1:
        index = 1
        for doc in res:
            print(str(index) + ") " + doc['identifier'] + " - " + doc['value'])
            index += 1

        desired_index = None
        while desired_index is None:
            desired_index = input("\nMultiple results, select desired gene[1-"+str(count)+"]:")
            if not desired_index.isdigit() or int(desired_index)<1 or int(desired_index)>count:
                print("Please enter # for one of the results above...")
                desired_index = None

        gene = res[int(desired_index) - 1]
    elif count == 1:
        gene = res[0]
    else:
        print("\nNo results found for query: '" + search_string + "'")
        return

    print("\nYou have selected:")
    print(gene)
    input("\nPress enter to query associated data with this gene...")
    clear_screen()
    print("Querying...")
    edge_res = query_edges(gene['identifier'])

    # Self
    GrG = query_associated_data(edge_res, 'Gr>G', db.genes)
    GcG = query_associated_data(edge_res, 'GcG', db.genes)
    GiG = query_associated_data(edge_res, 'GiG', db.genes)

    # Incoming Compound Edges
    CuG = query_associated_data(edge_res, 'CuG', db.compounds, 'source_id')
    CdG = query_associated_data(edge_res, 'CdG', db.compounds, 'source_id')
    CbG = query_associated_data(edge_res, 'CbG', db.compounds, 'source_id')

    # Incoming Disease Edges
    DuG = query_associated_data(edge_res, 'DuG', db.diseases, 'source_id')
    DdG = query_associated_data(edge_res, 'DdG', db.diseases, 'source_id')
    DaG = query_associated_data(edge_res, 'DaG', db.diseases, 'source_id')

    # Incoming Anatomy Edges
    AuG = query_associated_data(edge_res, 'AuG', db.anatomy, 'source_id')
    AdG = query_associated_data(edge_res, 'AdG', db.anatomy, 'source_id')
    AeG = query_associated_data(edge_res, 'AeG', db.anatomy, 'source_id')

    clear_screen()
    # Printing results
    print("==== " + gene['identifier'] + " ====")
    print("Name: " + gene['value'])

    print("==== Self Edge ====")
    print("Regulates (Gr>G)")
    for reg in GrG:
        print_associated_results(reg)
    print("Covaries (GcG)")
    for cov in GcG:
        print_associated_results(cov)
    print("Interacts (GiG)")
    for inter in GiG:
        print_associated_results(inter)
    print("==== Outgoing Edge ====")
    print("*NONE*")

    print("==== Incoming Compound Edge ====")
    print("Upregulated by Compound (CuG):")
    for upreg in CuG:
        print_associated_results(upreg)
    print("Downregulated by Compound (CdG):")
    for downreg in CdG:
        print_associated_results(downreg)
    print("Binded by Compound (CbG):")
    for binds in CbG:
        print_associated_results(binds)

    print("==== Incoming Disease Edge ====")
    print("Upregulated by Disease (DuG):")
    for upreg in DuG:
        print_associated_results(upreg)
    print("Downregulated by Disease (DdG):")
    for downreg in DdG:
        print_associated_results(downreg)
    print("Associated by Disease (DaG):")
    for assoc in DaG:
        print_associated_results(assoc)

    print("==== Incoming Anatomy Edge ====")
    print("Upregulated by Anatomy (AuG):")
    for upreg in AuG:
        print_associated_results(upreg)
    print("Downregulated by Anatomy (AdG):")
    for downreg in AdG:
        print_associated_results(downreg)
    print("Expressed by Anatomy (AeG):")
    for exp in AeG:
        print_associated_results(exp)

def query_missing_compound_diseases():
    res = n4j_compound_disease()

    input('Press enter to view results....')


'''
MAIN PROGRAM LOOP
- Prints main menu
- Calls collection query function based on user selection
'''

user_input = "0"
while user_input is not "6":
    print_menu()
    user_input = input("\nInput(1-6):")
    if user_input is not "6":
        os.system('cls' if os.name == 'nt' else 'clear')
        if user_input is "1":
            query_compound_nodes()
        elif user_input is "2":
            query_disease_nodes()
        elif user_input is "3":
            query_anatomy_nodes()
        elif user_input is "4":
            query_gene_nodes()
        elif user_input is "5":
            query_missing_compound_diseases()
        else:
            print("Unsupported option.")

        input("\n\nPress enter to continue...")


'''
TODO: Implement the below two cypher query options:
MATCH (c:Compound)-[:UP_REGULATES]->(:Gene)<-[:DOWN_REGULATES]-(:Anatomy)<-[:LOCALIZES]-(d:Disease) WHERE NOT (c)-[:TREATS]->(d) RETURN DISTINCT c.name, d.name ORDER BY c.name
MATCH (c:Compound)-[:DOWN_REGULATES]->(:Gene)<-[:UP_REGULATES]-(:Anatomy)<-[:LOCALIZES]-(d:Disease) WHERE NOT (c)-[:TREATS]->(d) RETURN DISTINCT c.name, d.name ORDER BY c.name
'''

clear_screen()
