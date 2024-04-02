from neo4j import GraphDatabase
import create_network as CN
class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response

import pandas as pd
d = {'c_id': ['c01104', 'c00565'], 'name': ['TMAO', 'TMA'], 'origin': ['yellow', 'blue']}
r = {'compound1':['c00565'], 'compound2':['c01104'], 'reaction': ['r02560'], 'KOs': ['K07811, K07812']}
df = pd.DataFrame(data=d)
rel_df  = pd.DataFrame(data=r)


conn = Neo4jConnection(uri="neo4j+s://9a835c85.databases.neo4j.io", 
                       user="neo4j",              
                       pwd="jNhhyfucYQOhm1qXgcLb2gzC6EPZVh0esuzXmBVTUXs")

#CN.add_compound(df, conn)
CN.add_relationship(rel_df, conn)

