from neo4j import GraphDatabase
import os 
import output_readins as OutRead
import create_nodes_edges as CNE 
import create_network as CN

# code to create neo4j connection taken from: https://towardsdatascience.com/create-a-graph-database-in-neo4j-using-python-4172d40f89c4
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


# directory where data is 
data_directory = '/Users/burkhang/Code_Projs/AMON/test_results'

# file names for KEGG outputs
file_names = ['rn_dict.json', 'ko_dict.json', 'co_dict.json']

# file path for amon mapper output 
amon_file = os.path.join(data_directory, 'kegg_mapper.tsv')


# Outputs needed for network creation: kegg and amon 
amon_o = OutRead.amon_mapper_output(data_directory, amon_file)
kegg_o = OutRead.get_KEGG_outputs(data_directory, file_names)

# getting nodes and edges in pandas dataframe formats
nodes_df = CNE.create_nodes_df(kegg_o, amon_o)
edges_df = CNE.create_edges_df(kegg_o, nodes_df)

# establishing connecton with neo4j
conn = Neo4jConnection(uri="neo4j+s://9a835c85.databases.neo4j.io", 
                            user="neo4j",              
                            pwd="jNhhyfucYQOhm1qXgcLb2gzC6EPZVh0esuzXmBVTUXs")

# create network in neo4j 
CN.add_compound(nodes_df, conn)
CN.add_relationship(edges_df, conn)



# import pandas as pd
# d = {'c_id': ['c01104', 'c00565'], 'name': ['TMAO', 'TMA'], 'origin': ['yellow', 'blue']}
# r = {'compound1':['c00565'], 'compound2':['c01104'], 'reaction': ['r02560'], 'KOs': ['K07811, K07812']}
# df = pd.DataFrame(data=d)
# rel_df  = pd.DataFrame(data=r)
#CN.add_compound(df, conn)
#CN.add_relationship(rel_df, conn)

