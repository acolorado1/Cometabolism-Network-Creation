# TODO: add node to graph 
def add_compound(compounds, conn):
    # adds compound nodes to the neo4j graph
    query = '''
            UNWIND $rows AS row 
            MERGE (n:Compound {id: row.c_id, name: row.name, origin: row.origin})
            '''
    return conn.query(query, parameters = {'rows':compounds.to_dict('records')})

# TODO: add relationships between nodes 
def add_relationship(relationships, conn):
    query = '''
            UNWIND $rows AS row
            MATCH (a: Compound{id:row.compound1}), 
                  (b: Compound{id:row.compound2})
            MERGE (a)-[r: BECOMES {Reaction: row.reaction, KOs: row.KOs}]->(b)
            '''
    return conn.query(query, parameters = {'rows':relationships.to_dict('records')})

# this is the query that can grab the co-metabolism patterns 
# does not matter the order of the colors 
def get_pattern(conn):
    query = '''
            MATCH p=({origin:"blue"})--({origin:"yellow"}) RETURN p
            '''
    return conn.query(query)