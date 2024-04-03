import pandas as pd

def create_nodes_df (KEGG_outputs:list, amon_mapper: dict): 
    """Takes KEGG outputs and AMON mapper output to create a pandas dataframe
        that will be used to create nodes 

    Args:
        KEGG_outputs (list): list of dictionaries encoding reactions, KOS, and compounds
        amon_mapper (dict): dictionary of compounds and their mapped origins by AMON

    Returns:
        pandas dataframe: dataframe containing compound id, name of compound, and origin
    """

    compounds = KEGG_outputs[2]

    # dictionary to be converted to pandas df
    compound_dict = {'c_id': [],
                     'name': [],
                     'origin': []}

    for key in amon_mapper.keys():
        
        # key will be the c_id (KEGG compound ID)
        if key[0] == 'C':
            origin = amon_mapper[key]

            # make sure compound in mapper has compound in amon output
            if key in compounds.keys():
                name = compounds[key]['NAME']
                compound_dict['c_id'].append(key)
                compound_dict['name'].append(name)
                compound_dict['origin'].append(origin)

    df = pd.DataFrame(data=compound_dict)

    return df

def create_edges_df(KEGG_outputs:list, nodes):
    """Takens in reaction info and converts into pandas dataframe information to
        for edges in the network 

    Args:
        KEGG_outputs (list): list of dicts that have KEGG reaction, KO, and compound info
        nodes (pandas daaframe): pandas dataframe containing node information 

    Returns:
        pandas dataframe: dataframe containing reactants and products, the reaction id and 
        the KOs associated with the reaction
    """
    reactions = KEGG_outputs[0]
    compounds = nodes['c_id'].tolist()

    # dictionary to be converted into pandas dataframe 
    edges_dict = {'compound1': [], 
                  'compound2': [],
                  'reaction': [],
                  'KOs': []}
    
    # each key is a reaction id from KEGG
    for key in reactions.keys():
        rn_info_dict = reactions[key]
        equation = rn_info_dict['EQUATION']
        
        # get compound from reactant side of equation
        for reactant in equation[0]: 

            # get compound from product side of equation 
            for product in equation[1]: 

                # ensure both product and reactant are nodes 
                if reactant in compounds and product in compounds: 
                    edges_dict['compound1'].append(reactant)
                    edges_dict['compound2'].append(product)
                    edges_dict['reaction'].append(key)

                    # get KOs 
                    orthology = rn_info_dict['ORTHOLOGY']
                    KOs = []
                    for index in range(0,len(orthology)): 
                        KOs.append(orthology[index][0])
                    edges_dict['KOs'].append(','.join(KOs))
    
    # convert to pandas dataframe
    df = pd.DataFrame(data = edges_dict)

    return df

