"""
This file will serve as the main user interface with the db
"""
from db_helper import get_client, query_data

DATABASE = 'csci79525_proj1'

db_client = get_client()
db = db_client[DATABASE]

res = query_data({}, db.genes, 10)

for doc in res:
    print(doc)
