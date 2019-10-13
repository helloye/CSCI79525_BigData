from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))

if driver:
    print('Connection established!!')
    print(driver)
