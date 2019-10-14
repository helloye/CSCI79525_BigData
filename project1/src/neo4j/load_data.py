import csv
from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'

try:
    driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))
    print('Neo4j Connection Established!!')
except:
    print('Neo4j Connection Error: ' + uri)

with open('../../data/nodes.tsv') as tsvin:
    reader = csv.reader(tsvin, delimiter='\t')
    count = 0
    for row in reader:
        # print(row)
        if count is 0:
            print(row)
        count += 1

"""
Need to extract both node and edge files into memory and then create the graph.
"""