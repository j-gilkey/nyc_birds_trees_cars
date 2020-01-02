import mysql_functions
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_tree_dataframe():
    data =  mysql_functions.get_all_trees_agg()
    #retrieve data stored in MySQL

    df = pd.DataFrame(data)

    return df

#print(create_tree_dataframe())
