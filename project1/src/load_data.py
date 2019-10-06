import csv

# Loading nodes...
with open('../data/nodes.tsv') as tsvin:
    reader = csv.reader(tsvin, delimiter='\t')
    for row in reader:
        print(row)

# Loading edges...
with open('../data/edges.tsv') as tsvin:
    reader = csv.reader(tsvin, delimiter='\t')
    for row in reader:
        print(row)

tsvin.close()
