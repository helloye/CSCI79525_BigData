# CSCI79525_BigData
Projects Repo for Hunter College CSCI79525 - FA 19

`./src/mongodb` - Contains source code to clean and load data into mongo db.

`./src/neo4j` - Contains source code to clean and load data into neo4j db.

`./src/user_interface.py` - Script to run the CLI to interact with the data.

See specific instructions below to load data into the respective db's.

Both sets of source code uses `Python 3.7.3` to interface with the db and to extract/load the data in the db. Please ensure you have the correct version installed. 

---

### Running MongoDB Load Data

Pre-requisite:
- Have `mongodb` installed and the daemon running, allowing for connection at the default `localhost:27017`
  - See installation instruction here: https://docs.mongodb.com/manual/administration/install-community/
- Have `pymongo` library installed to interface with `mongodb`.
  - Install `pymongo` using pip: `pip install pymongo`
  
Run instructions:
- Assuming you are in this dir (`/project1/src/mongo_db`)
  - To load data run: `python load_data.py`
    - This might take a while, especially loading the edges.

### Running Neo4J Load Data

Pre-req:
- Neo4j Community Edition: https://neo4j.com/download-center/#community
  - Used `Neo4j Community Edition 3.5.11`
  - This version requires `Java 8`!!
- Python Bolt driver for neo4j
  - Official Python library for interfacing with neo4j
  - https://neo4j.com/docs/api/python-driver/current/#installation
   
Optional Pre-req
- Neo4j Desktop https://neo4j.com/download/
  - Used to help interface with neo4j dbs.
  
Run instructions:
- Assuming you are in this dir (`/project1/src/neo4j`)
  - First you'll need to clean the data: `python clean_data.py`
  - It'll ask you to enter the location of the neo4j import folder. Enter the ABSOLUTE path of the import folder location. (ex: `/<ABSOLUTE_PATH>/neo4j-community-3.5.11/import'`)
  - This script will clean up the data into CSV format, ready to be loaded into neo4j using the load CSV tool.
- Once the above script is done running, run the load data script: `python load_data.py`

---

### CLI Manual
- Assuming you are in the root src directory: (`/project1/src`)
  - Simply run the UI python script to start up the CLI: `python user_interface.py`
- Usage is pretty straight forward if you follow the on screen prompt, but details are listed below:
  - `Options 1-4` queries MongoDB to retrieve documents with data on the different nodes (Compound, Disease, Anatomy, Gene)
    - This can be use to answer question #1 listed in the project spec by selecting the "Disease" (option 2)
 to list the different compounds that can treat it, and how it associates to other nodes.
    - If a query returns multiple results, the user will need to select from the list of results to query the desired datas.
  - `Option 5` queries Neo4j to uncover the missing edges/relationships between compounds and their respective diseases that they can potentially treat.
    - The query will return a list of `n` compounds that it finds that has at least one disease that it can potentially treat.
    - User will need to select the desired compound and look at the list of potential diseases that it can treat. Listing them all at once is too much, thus this sub-menu/option flow had to be implemented, similar to viewing multiple results in options 1-4 above.

---

### Queries Executed

#### MongoDB Queries
(Pre) Clean by dropping db using python mongodb client
`db_client.drop_database(db)`

Loading Nodes
```$xslt
db.<NodeType>.insertMany({
  "identifier": <NODE_ID>,
  "value": <NODE_VALUE>
  "type": <NODE_TYPE>})
```

Loading Edges
```$xslt
db.edges.insertMany({
  "source_id": <SOURCE_NODE_ID>,
  "edge_type": <EDGE_TYPE>
  "target_id": <TARGET_NODE_ID>})
```

Querying Nodes (user input regex)
```$xslt
{'$or': [{'identifier': {'$regex': re.compile('<USER_INPUT>', re.IGNORECASE)}},
{'value': {'$regex': re.compile('<USER_INPUT>', re.IGNORECASE)}}]}
```

Querying Node (single node)
```$xslt
{'identifier': '<SELECTED_NODE>', 'value': '<SELECTED_VALUE>', 'type': '<SELECTED_NODE_TYPE>'}
```
This query above is repeated multiple times for different edge node types (resembles, up regulates, treats, localizes, etc...)


#### Neo4J Queries
Loading Nodes (CSV Loader)
```$xslt

```