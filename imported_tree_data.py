# import packages/modules
import pandas as pd
import mysql.connector
import config
import mysql_functions as my_funcs
from sodapy import Socrata
from geopy.distance import geodesic
import random

pd.set_option('display.max_columns', None)

# def tree_paginate_2015():
#     tree_data = get_2015_trees()
#     tree_15_tuples = parse_2015(tree_data)
#
#     #n = 1000
#     #trees_15_chunks = [tree_15_tuples[i:i+n] for i in range(0,len(tree_15_tuples),n)]
#
#     #for chunk in trees_15_chunks:
#         #my_funcs.insert_tree_2015(chunk)
#
# def get_2015_trees():
# # make API call for 2015 tree data
#     client = Socrata("data.cityofnewyork.us", 'tree_key')
#     client = Socrata('data.cityofnewyork.us',
#                       config.tree_token_15,
#                       username=config.od_user,
#                       password=config.od_pw)
#     results15 = client.get("5rq2-4hqu", limit=4000)
#     tree_data_15 = pd.DataFrame.from_records(results15)
#     return tree_data_15
#
def get_neighbors(tree_loc, spc, df):
    #gets geodesic distance between singular tree and a group of trees. Then filters down to trees within 1000 feet. Note that each tree is a neighbor of itself
    df['distance'] = df.apply(lambda row: geodesic(row['loc_tuple'], tree_loc).feet,  axis = 1)
    neighbors_df = (df[df['distance'] < 500])
    #print('here 2')
    neighbor_tuple = (neighbors_df.shape[0], neighbors_df['spc_latin'].nunique(), neighbors_df[neighbors_df['spc_latin'] == spc].shape[0])
    #neighbor tuple consists of (total_neighbors, distinct species neighbors, same species neighbors)
    return neighbor_tuple

def apply_neighbors(df):
    df['loc_tuple'] = df.apply(lambda row: (row['latitude'], row['longitude']), axis = 1)
    print('here 1')
    print(df.shape)
    df[['total_neighbors', 'distinct_spc_neighbors', 'same_spc_neighbors']] = df.apply(lambda row: pd.Series(get_neighbors(row['loc_tuple'], row['spc_latin'], df[df['zipcode'] == row['zipcode']])), axis = 1)
    #df[['total_neighbors', 'distinct_spc_neighbors', 'same_spc_neighbors']] = df.apply(lambda row: pd.Series(get_neighbors(row['loc_tuple'], row['spc_latin'], df[df['zip_new'] == row['zip_new']])), axis = 1)
    df_insert = df[['total_neighbors', 'distinct_spc_neighbors', 'same_spc_neighbors', 'tree_id']]
    return df

def draw_sample(year, borough = 'any', zip_code = 'any'):
    table = 'trees_' + str(year)
    if zip_code == 'any':
        zip_list = my_funcs.get_zip_list(table, borough)
        zip_code = random.sample(zip_list, 1)[0]
    else:
        zip_code = str(zip_code)
    zip_df = pd.DataFrame(my_funcs.get_data_by_zip(str(zip_code), table), columns = ['tree_id', 'health', 'spc_latin', 'zipcode', 'boroname', 'latitude', 'longitude'])
    print(zip_df)
    zip_df = apply_neighbors(zip_df)
    print(zip_df)
    zip_tuples = list(zip_df[['total_neighbors', 'distinct_spc_neighbors', 'same_spc_neighbors', 'tree_id']].itertuples(index=False, name=None))
    print(zip_tuples)
    my_funcs.update_neighbor_values(zip_tuples,table)

    return

def draw_10_zips():
    for i in range(9):
        draw_sample('2015')
        print(i)
    print('Done now')

#print (draw_ten_samples('2005', 'Queens'))

draw_sample('2005', 'Queens', 'any')


#
#
# def parse_2015(tree_data_15):
#     # select all rows and only the columns wanted
#     trees_15 = pd.DataFrame(tree_data_15.loc[:, ['tree_id', 'health', 'spc_latin', 'spc_common', 'address', 'zipcode', 'cb_num', 'boroname', 'latitude', 'longitude']])
#     trees_15 = trees_15.dropna()
#     trees_15['loc_tuple'] = trees_15.apply(lambda row: (row['latitude'], row['longitude']), axis = 1)
#     trees_15[['total_neighbors', 'distinct_spc_neighbors', 'same_spc_neighbors']] = trees_15.apply(lambda row: pd.Series(get_neighbors(row['loc_tuple'], row['spc_latin'], trees_15[trees_15['zipcode'] == row['zipcode']])), axis = 1)
#     #creates the neighbor set of columns by passing each row as well as a subset of the dataframe that matches the zipcode of the current row to get_neighbors
#     print('total finished')
#     trees_15_tuples = list(trees_15.itertuples(index=False, name=None))
#     return trees_15_tuples

#tree_paginate_2015()

# make API call for 1995 tree data
def get_1995_with_diameter(zipcode):
    client = Socrata("data.cityofnewyork.us", 'tree_key')
    client = Socrata('data.cityofnewyork.us',
                      config.tree_token_95,
                      username=config.od_user,
                      password=config.od_pw)
    results95 = client.get("kyad-zm4j", limit=600000)
    tree_data_95 = pd.DataFrame.from_records(results95)

    # select all rows and only the columns wanted
    tree_data_95 = tree_data_95.dropna()
    tree_data_95 = tree_data_95[tree_data_95['zip_new'] == zipcode]
    tree_data_95 = pd.DataFrame(tree_data_95.loc[:, ['recordid', 'condition', 'spc_latin', 'spc_common', 'address', 'zip_new', 'borough', 'latitude', 'longitude']])
    # tree_data_95['loc_tuple'] = tree_data_95.apply(lambda row: (row['latitude'], row['longitude']), axis = 1)
    # tree_data_95[['total_neighbors', 'distinct_spc_neighbors', 'same_spc_neighbors']] = tree_data_95.apply(lambda row: pd.Series(get_neighbors(row['loc_tuple'], row['spc_latin'], tree_data_95[tree_data_95['zip_new'] == row['zip_new']])), axis = 1)

    tree_data_95 = apply_neighbors(tree_data_95)

    return tree_data_95

#print(get_1995_with_diameter('10007'))
