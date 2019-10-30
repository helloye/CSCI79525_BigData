"""
Utility helper functions to insert into db.
Mostly mongo client.
"""
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from neo4j import GraphDatabase


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


def n4j_compound_disease():
    uri = 'bolt://localhost:7687'
    try:
        driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))
        print('Neo4j Connection Established!!')
    except:
        print('Neo4j Connection Error: ' + uri)

    results = dict()

    with driver.session() as session:

        # UP_REGULATES -> Gene <- DOWN_REGULATES
        print('\n Running Neo4j UP->Gene<-DOWN Query:'
              '\n MATCH (c:Compound)-[:UP_REGULATES]->(:Gene)<-[:DOWN_REGULATES]-(:Anatomy)<-[:LOCALIZES]-(d:Disease)'
              '\n WHERE NOT (c)-[:TREATS]->(d) RETURN DISTINCT c.name, d.name ORDER BY c.name')

        query_string = "MATCH (c:Compound)-[:UP_REGULATES]->(:Gene)<-[:DOWN_REGULATES]-(:Anatomy)<-[:LOCALIZES]-(d:Disease) WHERE NOT (c)-[:TREATS]->(d) RETURN DISTINCT c.name, d.name ORDER BY c.name"
        records = session.run(query_string).records()

        for r in records:
            compound = r['c.name']
            disease = r['d.name']
            if compound not in results:
                results[compound] = []

            results[compound].append(disease)

        # DOWN_REGULATES -> Gene <- UP_REGULATES
        print('\n\n Running Neo4j DOWN->Gene<-UP Query:'
              '\n MATCH (c:Compound)-[:DOWN_REGULATES]->(:Gene)<-[:UP_REGULATES]-(:Anatomy)<-[:LOCALIZES]-(d:Disease)'
              '\n WHERE NOT (c)-[:TREATS]->(d) RETURN DISTINCT c.name, d.name ORDER BY c.name')

        query_string = "MATCH (c:Compound)-[:DOWN_REGULATES]->(:Gene)<-[:UP_REGULATES]-(:Anatomy)<-[:LOCALIZES]-(d:Disease) WHERE NOT (c)-[:TREATS]->(d) RETURN DISTINCT c.name, d.name ORDER BY c.name"
        records = session.run(query_string).records()

        for r in records:
            compound = r['c.name']
            disease = r['d.name']
            if compound not in results:
                results[compound] = []

            if disease not in results[compound]:
                results[compound].append(disease)

    input('\n\nPress enter to view results....\n')
    return results


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
