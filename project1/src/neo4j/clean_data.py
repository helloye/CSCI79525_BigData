import re, os


# Actual User Input
# output_path = input("Path to output converted CSV:")

# Testing
output_path = '/Users/helloye/Documents/CSCI/neo4j-community-3.5.11/import'

"""
CONVERT TSV TO CSV FOR LOAD_CSV
"""

# Convert Nodes
node_csv_data = {"Compound": [], "Disease": [], "Anatomy": [], "Gene": []}

nodes_file_total_lines = sum(1 for line in open('../../data/nodes.tsv'))
count = 0
with open('../../data/nodes.tsv', 'r') as tsvin:
    for line in tsvin:
        if count > 1:
            converted_line = re.sub("\t", ",", line)
            converted_data = converted_line.split(",")
            key = converted_data[2].strip()
            node_csv_data[key].append(converted_line.rstrip())
        count += 1
        print("Nodes Conversion Progress: " + str(count) + "/" + str(nodes_file_total_lines))
tsvin.close()


for key in node_csv_data:
    filename = output_path+"/"+key+".csv"
    with open(filename, 'w') as f:
        f.write("id,name,type\n")
        for line in node_csv_data[key]:
            f.write(line + "\n")
        print("Loaded: " + filename)
    f.close()


input("Converted Nodes. Press enter to start edge conversion...")
os.system('cls' if os.name=='nt' else 'clear')


# Convert Edges
edge_csv_data = {
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
            edge_csv_data[key].append(converted_line.rstrip())
        count += 1
        print("Edges Conversion Progress: " + str(count) + "/" + str(edges_file_total_lines))
tsvin.close()


for key in edge_csv_data:
    if key == "Gr>G":
        key = "GrG"
    filename = output_path+"/"+key+".csv"
    with open(filename, 'w') as f:
        f.write("source,edge,target\n")
        for line in edge_csv_data[key]:
            f.write(line + "\n")
        print("Loaded: " + filename)
    f.close()

input("Converted Edges. Press enter to end conversion...")
os.system('cls' if os.name=='nt' else 'clear')
