import os 
import output_readins as OutRead

# directory where data is 
data_directory = '/Users/burkhang/Code_Projs/AMON/test_results'

# file names for KEGG outputs
file_names = ['rn_dict.json', 'ko_dict.json', 'co_dict.json']

# file path for amon mapper output 
amon_file = os.path.join(data_directory, 'kegg_mapper.tsv')


# Outputs needed for network creation: kegg and amon 
amon_o = OutRead.amon_mapper_output(data_directory, amon_file)
kegg_o = OutRead.get_KEGG_outputs(data_directory, file_names)

rxns_dict = kegg_o[0]
rxns_keys = rxns_dict.keys()
for key in rxns_keys: 
    rxn_value_dict = rxns_dict[key]
    print(rxn_value_dict['DBLINKS'])
