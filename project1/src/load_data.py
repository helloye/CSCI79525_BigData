import csv

# Loading nodes...
with open('../data/nodes.tsv','rb') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    for row in tsvin:
        print(row)

# Loading edges...
with open('../data/edges.tsv','rb') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    for row in tsvin:
        print(row)