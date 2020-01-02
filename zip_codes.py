from uszipcode import SearchEngine
import mysql_functions
import tree_data_frame_creation as tree

search = SearchEngine(simple_zipcode=True)

all_zip_codes = list(tree.create_tree_dataframe().zipcode.unique())

print(all_zip_codes)
