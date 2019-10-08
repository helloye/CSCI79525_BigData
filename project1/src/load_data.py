import csv
from db_helper import get_client, insert_data

db_client = get_client()
db = db_client.test

# Loading nodes...
with open('../data/nodes.tsv') as tsvin:
    reader = csv.reader(tsvin, delimiter='\t')
    for row in reader:
        data_type = row[2]
        data = {
            "identifier": row[0],
            "value": row[1],
            "type": data_type
        }
        print("Inserting::" + str(data))
        if data_type == "Anatomy":
            insert_data(data, db.anatomy)
        if data_type == "Gene":
            insert_data(data, db.gene)
        if data_type == "Disease":
            insert_data(data, db.disease)

# Loading edges...there are a lot!!!
with open('../data/edges.tsv') as tsvin:
    reader = csv.reader(tsvin, delimiter='\t')
    count = 0
    for row in reader:
        if count > 0:
            data = {
                "source_id": row[0],
                "edge_type": row[1],
                "target_id": row[2]
            }
            if count % 10000 == 0:
                print("Inserting Edge(" + str(count) + "):: " + str(data))

            insert_data(data, db.edges)

        count += 1

tsvin.close()
