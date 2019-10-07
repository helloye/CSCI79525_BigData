import csv
from db_helper import get_client

dbClient = get_client()

# Loading nodes...
with open('../data/nodes.tsv') as tsvin:
    reader = csv.reader(tsvin, delimiter='\t')
    for row in reader:
        id_data = row[0].split('::')
        print(id_data)
        print(row[0] + " - " + row[1] + " - " + row[2] + "\n")

# Loading edges...
with open('../data/edges.tsv') as tsvin:
    reader = csv.reader(tsvin, delimiter='\t')
    for row in reader:
        print(row)

tsvin.close()
