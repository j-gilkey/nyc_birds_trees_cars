import mysql_functions
import pandas as pd
import seaborn as sns
import tree_data_frame_creation
import zip_data_frame
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

tree_df = tree_data_frame_creation.create_distinct_tree_dataframe()
print(tree_df)
tree_df = tree_df[tree_df['year'] == '2015']
print(tree_df)
zip_df = zip_data_frame.create_zip_dataframe()

big_df = pd.merge(tree_df, zip_df, on = 'zipcode', how='inner')

print(big_df)
