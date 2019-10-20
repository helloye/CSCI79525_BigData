print('HELLO NEO4J UI')

"""
Notes:
1) Should probably use Disease/Compound for a base search as we are concerned about finding the hidden edge
   between these two nodes.

2) Sample possible query:
MATCH (c:Compound)-[:DOWN_REGULATES]->(g:Gene)<-[:UP_REGULATES]-(a:Anatomy)<-[:LOCALIZES]-(d:Disease) RETURN c,g,a,d LIMIT 25
"""