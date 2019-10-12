"""
This file parses the 2 tsv files in the data folder and inserts
the data into the database
"""
import csv
from db_helper import get_client, insert_data, drop_db, insert_progress_printer

# Actual
DATABASE = 'csci79525_proj1'

# Test
# DATABASE = 'test'


db_client = get_client()
# Clean db before loading new data
drop_db(db_client, DATABASE);

db = db_client[DATABASE]

# Loading nodes...
node_file_total_lines = sum(1 for line in open('../../data/nodes.tsv'))
with open('../../data/nodes.tsv') as tsvin:
    reader = csv.reader(tsvin, delimiter='\t')
    count = 0
    for row in reader:
        if count > 0:
            data_type = row[2]
            data = {
                "identifier": row[0],
                "value": row[1],
                "type": data_type
            }
            if data_type == "Compound":
                insert_data(data, db.compounds)
            if data_type == "Anatomy":
                insert_data(data, db.anatomy)
            if data_type == "Gene":
                insert_data(data, db.genes)
            if data_type == "Disease":
                insert_data(data, db.diseases)

        count += 1
        insert_progress_printer(node_file_total_lines, count, 'Node Insert', 300, True)
    insert_progress_printer(node_file_total_lines, count, 'Node Insert', 1, True)


# Loading edges: 1.3mil count
edges_file_total_lines = sum(1 for line in open('../../data/edges.tsv'))
with open('../../data/edges.tsv') as tsvin:
    reader = csv.reader(tsvin, delimiter='\t')
    count = 0
    print("\n\nInserting Edges...this could take a while....\n\n")
    for row in reader:
        if count > 0:
            data = {
                "source_id": row[0],
                "edge_type": row[1],
                "target_id": row[2]
            }

            insert_data(data, db.edges)

        count += 1
        insert_progress_printer(edges_file_total_lines, count, 'Edges Insert', 1, False)
    insert_progress_printer(node_file_total_lines, count, 'Node Insert', 1, False)

tsvin.close()
