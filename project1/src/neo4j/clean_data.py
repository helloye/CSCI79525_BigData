import re

"""
CONVERT TSV TO CSV FOR LOAD_CSV
Write to different CSV files based on edge relation type
"""
csv_data = {
    # Compound Source
    "CrC": [], "CtD": [], "CpD": [], "CuG": [], "CdG": [], "CbG": [],
    # Disease Source
    "DrD": [], "DlA": [], "DuG": [], "DdG": [], "DaG": [],
    # Anatomy Source
    "AuG": [], "AdG": [], "AeG": [],
    # Gene Source
    "GrG": [], "GcG": [], "GiG": [],
}

edges_file_total_lines = sum(1 for line in open('../../data/edges.tsv'))
count = 0
with open('../../data/edges.tsv', 'r') as tsvin:
    for line in tsvin:
        if count > 1:
            converted_line = re.sub("\t", ",", line)
            converted_data = converted_line.split(",")
            key = converted_data[1]
            if key == "Gr>G":
                key = "GrG"
            csv_data[key].append(converted_line.rstrip())
            print("Conversion Progress: " + str(count) + "/" + str(edges_file_total_lines))
        count += 1
    tsvin.close()

# Actual User Input
# neo4j_import_folder = input("Absolute path of Neo4j import folder:")

# Testing
neo4j_import_folder = '/Users/helloye/Documents/CSCI/neo4j-community-3.5.11/import'

for key in csv_data:
    if key == "Gr>G":
        key = "GrG"
    filename = neo4j_import_folder+"/"+key+".csv"
    with open(filename, 'w') as f:
        f.write("source,edge,target\n")
        for line in csv_data[key]:
            f.write(line + "\n")
        print("Loaded: " + filename)
    f.close()