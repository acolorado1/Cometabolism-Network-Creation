import json
import os


def get_KEGG_outputs (data_directory:str, file_names:list):
    """This function returns a list of dicts containing information gathered from KEGG

    Args:
        data_directory (str): file path to directory containing KEGG output json files 
        file_names (list): list of 3 strings that are names of json files output from AMON

    Returns:
        list: list of dictionaires containing KEGG outputs: reactions, KOs, compounds
    """

    # TODO 
    # error should be a list of strings 
    # create an error should files not be JSON formats 
    # list should have three items 

    # create empty list to add dictionaries too 
    KEGG_outputs = []

    # get compounds, reactions, and KOs 
    for file in file_names: 
        # create full path
        full_path = os.path.join(data_directory, file)

        # get JSON on KEGG reactions 
        with open(full_path, 'r') as rxn_file: 
            current_output = json.load(rxn_file)
            KEGG_outputs.append(current_output)

    return KEGG_outputs


def amon_mapper_output(data_directory: str, file: str):
    """load in AMON mapper output 

    Args:
        data_directory (str): directory containing the data 
        file (str): name of the mapper file 

    Returns:
        dict: dict where keys are KEGG ids and values are colors represnting microbe 
        or host origin 
    """
    # create full path
    file = os.path.join(data_directory, file)

    # initialize empty dict  
    map_o = {}

    # add mapping information line by line to dict
    with open(file) as f:
        for line in f: 
            split_line = line.split()
            
            # ignore first line 
            if len(split_line) > 1:
                map_o[split_line[0]] = split_line[1]

    return map_o 