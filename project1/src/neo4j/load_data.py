import csv, re
from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'

rel_to_query_data_map = {
    # Compound Source
    "CrC": {"match_type": "MATCH (a:Compound), (b:Compound)", "rel": "RESEMBLES"},
    "CtD": {"match_type": "MATCH (a:Compound), (b:Disease)", "rel": "TREATS"},
    "CpD": {"match_type": "MATCH (a:Compound), (b:Disease)", "rel": "PALLIATES"},
    "CuG": {"match_type": "MATCH (a:Compound), (b:Gene)", "rel": "UP_REGULATES"},
    "CdG": {"match_type": "MATCH (a:Compound), (b:Gene)", "rel": "DOWN_REGULATES"},
    "CbG": {"match_type": "MATCH (a:Compound), (b:Gene)", "rel": "BINDS"},
    # Disease Source
    "DrD": {"match_type": "MATCH (a:Disease), (b:Disease)", "rel": "RESEMBLES"},
    "DlG": {"match_type": "MATCH (a:Disease), (b:Anatomy)", "rel": "LOCALIZES"},
    "DuG": {"match_type": "MATCH (a:Disease), (b:Gene)", "rel": "UP_REGULATES"},
    "DdD": {"match_type": "MATCH (a:Disease), (b:Gene)", "rel": "DOWN_REGULATES"},
    "DaD": {"match_type": "MATCH (a:Disease), (b:Gene)", "rel": "ASSOCIATES"},
    # Anatomy Source
    "AuG": {"match_type": "MATCH (a:Anatomy), (b:Gene)", "rel": "UP_REGULATES"},
    "AdG": {"match_type": "MATCH (a:Anatomy), (b:Gene)", "rel": "DOWN_REGULATES"},
    "AeG": {"match_type": "MATCH (a:Anatomy), (b:Gene)", "rel": "EXPRESSES"},
    # Gene Source
    "Gr>G": {"match_type": "MATCH (a:Gene), (b:Gene)", "rel": "REGULATES"},
    "GcG": {"match_type": "MATCH (a:Gene), (b:Gene)", "rel": "COVARIES"},
    "GiG": {"match_type": "MATCH (a:Gene), (b:Gene)", "rel": "INTERACTS"},
}


def create_rel_query(s, r, t):
    query_data = rel_to_query_data_map[r]
    return query_data['match_type'] + " WHERE a.id='" + s + "' AND b.id='" + t + "' CREATE (a)-[r:" + query_data['rel'] + "]->(b)"


try:
    driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))
    print('Neo4j Connection Established!!')
except:
    print('Neo4j Connection Error: ' + uri)

compound_nodes = []
disease_nodes = []
anatomy_nodes = []
gene_nodes = []

with open('../../data/nodes.tsv') as tsvin:
    reader = csv.reader(tsvin, delimiter='\t')
    count = 0
    with driver.session() as session:
        # **WARNING** This will wipe all data in the graph db
        session.run("MATCH(n) DETACH DELETE n")
        count = 0
        for row in reader:
            query = ""
            if row[2] == 'Compound':
                compound_nodes.append(row)
                query = 'CREATE(:Compound {id:"'+row[0]+'",name: "'+row[1]+'"})'
            if row[2] == 'Disease':
                disease_nodes.append(row)
                query = 'CREATE(:Disease {id:"'+row[0]+'",name: "'+row[1]+'"})'
            if row[2] == 'Anatomy':
                anatomy_nodes.append(row)
                query = 'CREATE(:Anatomy {id:"'+row[0]+'",name: "'+row[1]+'"})'
            if row[2] == 'Gene':
                gene_nodes.append(row)
                query = 'CREATE(:Gene {id:"'+row[0]+'",name: "'+row[1]+'"})'

            if query != "":
                count += 1
                print(query)
                session.run(query)
        session.close()
        print(str(count) + " Nodes Created.\n")

edge_data = []
edges_file_total_lines = sum(1 for line in open('../../data/edges.tsv'))
with open('../../data/edges.tsv') as tsvin:
    reader = csv.reader(tsvin, delimiter='\t')
    count = 0
    print("Creating relationships...\n")
    with driver.session() as session:
        for row in reader:
            if count > 1:
                edge_data.append(row)
                source = row[0]
                rel = row[1]
                target = row[2]

                # TODO: Build relationship in memory and only insert the ones needed?
                rel_query = create_rel_query(source, rel, target)
                session.run(rel_query)

            count += 1
            if count % 100 == 0:
                print(str(count) + "/" + str(edges_file_total_lines))
    session.close()


# TODO: Build algorithm to create neo4j queries to insert relational graph into DB.
"""
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

"""