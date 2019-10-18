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

"""
LOADING NODES
"""
with driver.session() as session:
    for key in node_keys:
        query = "USING PERIODIC COMMIT 1000 " \
                "LOAD CSV WITH HEADERS FROM 'file:///"+key+".csv' AS row" \
                "\nCREATE(:"+key+" {id: row.id, name: row.name})"
        print("\nRunning Query:\n")
        print(query + "\n")
        session.run(query)
    session.run('CREATE CONSTRAINT ON (n:Compound) ASSERT (n.id) IS UNIQUE')
    session.run('CREATE CONSTRAINT ON (n:Disease) ASSERT (n.id) IS UNIQUE')
    session.run('CREATE CONSTRAINT ON (n:Anatomy) ASSERT (n.id) IS UNIQUE')
    session.run('CREATE CONSTRAINT ON (n:Gene) ASSERT (n.id) IS UNIQUE')
    session.run('CREATE INDEX ON :Compound(id)')
    session.run('CREATE INDEX ON :Disease(id)')
    session.run('CREATE INDEX ON :Anatomy(id)')
    session.run('CREATE INDEX ON :Gene(id)')
    session.close()

input("\n\nNodes added to graph. Press enter to continue adding edges...\n\n")


"""
LOADING EDGE RELATIONS
"""
# TESTING
# neo4j_import_folder = '/Users/helloye/Documents/CSCI/neo4j-community-3.5.11/import'

with driver.session() as session:
    for key in rel_to_query_data_map:
        # full_file_path = neo4j_import_folder + "/" + key + '.csv'
        rel_data = rel_to_query_data_map[key]
        query = "USING PERIODIC COMMIT 10000 " \
                "LOAD CSV WITH HEADERS FROM 'file:///"+key+".csv' AS row" \
                "\n" + rel_data['match_type'] + "\n" \
                "CREATE (a)-[:"+rel_data['rel']+" {" \
                "rel: row.edge, source: row.source, target: row.target" \
                "}]->(b)"
        print("\nRunning Query:\n")
        print(query)
        session.run(query)
session.close()

input("Edges added. Press enter to finish loading data....")
os.system('cls' if os.name=='nt' else 'clear')

"""
==== MY NOTES ====

Sample query:
1) Compound::DB00091 -Treates-> Disease::DOID:9074 -Localizes Anatomy-> Anatomy::UBERON:0000043 
2) Compound::DB00788 -Palliates-> Disease::DOID:9074

{id:"Compound::DB00091",name: "Cyclosporine"}
{id:"Disease::DOID:9074",name:"systemic lupus erythematosus"}
{id:"Anatomy::UBERON:0000043",name:"tendon"}

Cypher Query:

CREATE (c:COMPOUND {id:"Compound::DB00091",name:"Cyclosporine"})-[CtD:TREATES_DISEASE]->(d:Disease {id:"Disease::DOID:9074",name:"systemic lupus erythematosus"})-[DlA:LOCALIZES_ANATOMY]->(a:Anatomy {id:"Anatomy::UBERON:0000043",name:"tendon"})

- Multiple CREATE relational queries as the one above on the same NODE will result in multiple graphs.
-- i.e: Running the above query twice will create 2 sets of 3 nodes, each with their own unique relationships.

- Possible solution:
1) Create all nodes first.
CREATE(:Compound {id:"Compound::DB00091",name: "Cyclosporine"})

2) Then run through the edge_data list, and use the MATCH command to CREATE the edges between two MATCH'd nodes.
ex:
MATCH (c:Compound),(d:Disease)
WHERE c.id='Compound::DB00091' AND d.id='Disease::DOID:9074'
CREATE (c)-[r:TREATS_DISEASE]->(b)

* The above is the same as if we were to link it on CREATE:
CREATE (c:COMPOUND {id:"Compound::DB00091",name:"Cyclosporine"})-[CtD:TREATES_DISEASE]->(d:Disease {id:"Disease::DOID:9074",name:"systemic lupus erythematosus"})

*Utility Command Note*
MATCH(n) RETURN n - Returns all node in graph
MATCH(n) DETACH DELETE n - Deletes everything!!

neo4j Python Driver Transaction Reference Notes:
Reference: https://neo4j.com/docs/api/python-driver/current/transactions.html#transactions

10/14/19 - Note, visualizing ALL the nodes is REALLLYYYY EXPENSIVE. Look to limit it to the relation query to answer question 2 only...?

10/15/19 - Note, it's gonna take a long time to insert all the edges, look to filter in memory and only insert the ones that answer question 2?

Compound -Treats-> Disease 

10/16/19 - LOAD_CSV Query:
Assume sample_edges.csv is in the /import folder in neo4j server folder.

** NOTE DO NOT QUERY WITHOUT LABELS!!**

USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM 'file:///<FILE>.csv' AS row
MATCH (source:<SOURCE_LABEL> {id: row.source})
MATCH (target:<TARGET_LABEL> {id: row.target}) 
CREATE (source)-[:<RELATION_TYPE> {
rel: row.edge, source: row.source, target: row.target
}]->(target)

"""