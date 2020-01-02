import mysql_functions
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_distinct_tree_dataframe():
    data = mysql_functions.get_distinct_trees_by_zip()
    df = pd.DataFrame(data, columns = ['zipcode', 'boro', 'year', 'tree_count', 'distinct_species_count'])
    return df

def create_tree_dataframe_health():
    data =  mysql_functions.get_all_trees_with_health_agg()
    #retrieve data stored in MySQL

    df = pd.DataFrame(data, columns = ['zipcode', 'boro', 'healthy', 'year', 'tree_count'])

    return df

#print(create_tree_dataframe())


def box_plot(df):
    fig = plt.figure()
    plt.style.use('seaborn')
    sns.set_palette('colorblind')
    df = df.groupby(['zipcode', 'boro', 'year'])['tree_count', 'distinct_species_count'].sum()
    #print(df)
    ax = sns.catplot(x='boro', y='tree_count', hue= 'year', data=df, kind="box")
    plt.show()

#box_plot(create_tree_dataframe())


#df  = create_tree_dataframe()
#print(df)
#print(list(df.zipcode.unique()))
