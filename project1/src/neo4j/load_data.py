import pprint, os
from neo4j import GraphDatabase

pp = pprint.PrettyPrinter(indent=4)

node_keys = {"Compound", "Disease", "Anatomy", "Gene"}

rel_to_query_data_map = {
    # Compound Source
    "CrC": {"match_type": "MATCH (a:Compound {id: row.source})\nMATCH (b:Compound {id: row.target})",
            "rel": "RESEMBLES"},
    "CtD": {"match_type": "MATCH (a:Compound {id: row.source})\nMATCH (b:Disease {id: row.target})",
            "rel": "TREATS"},
    "CpD": {"match_type": "MATCH (a:Compound {id: row.source})\nMATCH (b:Disease {id: row.target})",
            "rel": "PALLIATES"},
    "CuG": {"match_type": "MATCH (a:Compound {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "UP_REGULATES"},
    "CdG": {"match_type": "MATCH (a:Compound {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "DOWN_REGULATES"},
    "CbG": {"match_type": "MATCH (a:Compound {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "BINDS"},
    # Disease Source
    "DrD": {"match_type": "MATCH (a:Disease {id: row.source})\nMATCH (b:Disease {id: row.target})",
            "rel": "RESEMBLES"},
    "DlA": {"match_type": "MATCH (a:Disease {id: row.source})\nMATCH (b:Anatomy {id: row.target})",
            "rel": "LOCALIZES"},
    "DuG": {"match_type": "MATCH (a:Disease {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "UP_REGULATES"},
    "DdG": {"match_type": "MATCH (a:Disease {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "DOWN_REGULATES"},
    "DaG": {"match_type": "MATCH (a:Disease {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "ASSOCIATES"},
    # Anatomy Source
    "AuG": {"match_type": "MATCH (a:Anatomy {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "UP_REGULATES"},
    "AdG": {"match_type": "MATCH (a:Anatomy {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "DOWN_REGULATES"},
    "AeG": {"match_type": "MATCH (a:Anatomy {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "EXPRESSES"},
    # Gene Source
    "GrG": {"match_type": "MATCH (a:Gene {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "REGULATES"},
    "GcG": {"match_type": "MATCH (a:Gene {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "COVARIES"},
    "GiG": {"match_type": "MATCH (a:Gene {id: row.source})\nMATCH (b:Gene {id: row.target})",
            "rel": "INTERACTS"},
}


def create_rel_query(s, r, t):
    query_data = rel_to_query_data_map[r]
    return query_data['match_type'] + " WHERE a.id='" + s + "' AND b.id='" + t + "' CREATE (a)-[r:" + query_data['rel'] + "]->(b)"

"""
MAIN PROGRAM STARTS HERE
"""

uri = 'bolt://localhost:7687'

try:
    driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))
    print('Neo4j Connection Established!!')
except:
    print('Neo4j Connection Error: ' + uri)

node_count = 0
edge_count = 0

with driver.session() as session:
    # Removing all data from DB ***
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Cleaning graph, deleting all data from neo4j db...")
    print("Running: MATCH(n) DETACH DELETE n\n")
    session.run("MATCH(n) DETACH DELETE n")
    """
    LOADING NODES
    """
    for key in node_keys:
        query = "USING PERIODIC COMMIT 1000 " \
                "LOAD CSV WITH HEADERS FROM 'file:///"+key+".csv' AS row" \
                "\nCREATE(n:"+key+" {id: row.id, name: row.name}) RETURN count(n)"
        print("\nRunning Query:\n")
        print(query + "\n")
        res = session.run(query)
        node_count += res.single()[0]
    session.run('CREATE CONSTRAINT ON (n:Compound) ASSERT (n.id) IS UNIQUE')
    session.run('CREATE CONSTRAINT ON (n:Disease) ASSERT (n.id) IS UNIQUE')
    session.run('CREATE CONSTRAINT ON (n:Anatomy) ASSERT (n.id) IS UNIQUE')
    session.run('CREATE CONSTRAINT ON (n:Gene) ASSERT (n.id) IS UNIQUE\n\n')

    input("Nodes added to graph. Press enter to continue adding edges...\n\n")

    """
    LOADING EDGE RELATIONS
    """

    for key in rel_to_query_data_map:
        # full_file_path = neo4j_import_folder + "/" + key + '.csv'
        rel_data = rel_to_query_data_map[key]
        query = "USING PERIODIC COMMIT 10000 " \
                "LOAD CSV WITH HEADERS FROM 'file:///"+key+".csv' AS row" \
                "\n" + rel_data['match_type'] + "\n" \
                "CREATE (a)-[e:"+rel_data['rel']+" {" \
                "rel: row.edge, source: row.source, target: row.target" \
                "}]->(b) RETURN count(e)"
        print("\nRunning Query:\n")
        print(query)
        res = session.run(query)
        edge_count += res.single()[0]
session.close()

input("\n\nEdges added. Press enter to continue....\n\n")
os.system('cls' if os.name == 'nt' else 'clear')
print(str(node_count) + " Nodes inserted.")
print(str(edge_count) + " Edges inserted.\n\n")
input("Press enter to finish loading data graph...")
os.system('cls' if os.name == 'nt' else 'clear')
