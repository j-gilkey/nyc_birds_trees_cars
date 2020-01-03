# import packages/modules
import pandas as pd
import mysql.connector
import config
import mysql_functions as my_funcs
from sodapy import Socrata

# set database name
DB_NAME = 'birds_trees_etc'

# create connection
cnx = mysql.connector.connect(
    host = config.host,
    user = config.user,
    passwd = config.password,
    database = DB_NAME,
    use_pure=True
    )

cursor = cnx.cursor()



# make API call for 2015 tree data
client = Socrata("data.cityofnewyork.us", 'tree_key')
client = Socrata('data.cityofnewyork.us',
                  config.tree_token_15,
                  username=config.od_user,
                  password=config.od_pw)
results15 = client.get("5rq2-4hqu", limit=690000)
tree_data_15 = pd.DataFrame.from_records(results15)

# select all rows and only the columns wanted, drop nans
trees_15 = pd.DataFrame(tree_data_15.loc[:, ['tree_id', 'health', 'spc_latin', 'spc_common', 'address', 'zipcode', 'boroname', 'latitude', 'longitude']])
trees_15 = trees_15.dropna()
print(trees_15.shape)

# parse tree data into tuples
trees_15_tuples = list(trees_15.itertuples(index=False, name=None))

# split list into smaller lists
n = 10000
trees_15_chunks = [trees_15_tuples[i:i+n] for i in range(0,len(trees_15_tuples),n)]


# insert into database
for chunk in trees_15_chunks:
    add_tree_15 = ("""INSERT INTO trees_2015
               (tree_id, health, spc_latin, spc_common, address, zipcode, boroname, lat, lng, total_neighbors, distinct_spc_neighbors, same_spc_neighbors)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL, NULL);""")

    cursor.executemany(add_tree_15, chunk)
    cnx.commit()




# make API call for 2005 tree data
client = Socrata("data.cityofnewyork.us", 'tree_key')
client = Socrata('data.cityofnewyork.us',
                  config.tree_token_05,
                  username=config.od_user,
                  password=config.od_pw)
results05 = client.get("29bw-z7pj", limit=600000)
tree_data_05 = pd.DataFrame.from_records(results05)

# select all rows and only the columns wanted, drop nans
trees_05 = pd.DataFrame(tree_data_05.loc[:, ['objectid', 'status', 'spc_latin', 'spc_common', 'address', 'zipcode', 'boroname', 'latitude', 'longitude']])
trees_05 = trees_05.dropna()
print(trees_05.shape)

# parse tree data into tuples
trees_05_tuples = list(trees_05.itertuples(index=False, name=None))

# split list into smaller lists
n = 20000
trees_05_chunks = [trees_05_tuples[i:i+n] for i in range(0,len(trees_05_tuples),n)]


# insert into database
for chunk in trees_05_chunks:
    add_tree_05 = ("""INSERT INTO trees_2005
               (tree_id, health, spc_latin, spc_common, address, zipcode, boroname, lat, lng)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""")

    cursor.executemany(add_tree_05, chunk)
    cnx.commit()




# make API call for 1995 tree data
client = Socrata("data.cityofnewyork.us", 'tree_key')
client = Socrata('data.cityofnewyork.us',
                  config.tree_token_95,
                  username=config.od_user,
                  password=config.od_pw)
results95 = client.get("kyad-zm4j", limit=600000)
tree_data_95 = pd.DataFrame.from_records(results95)

# select all rows and only the columns wanted, drop nans
trees_95 = pd.DataFrame(tree_data_95.loc[:, ['recordid', 'condition', 'spc_latin', 'spc_common', 'address', 'zip_new', 'borough', 'latitude', 'longitude']])
trees_95 = trees_95.dropna()
print(trees_95.shape)

# parse tree data into tuples
trees_95_tuples = list(trees_95.itertuples(index=False, name=None))

# split list into smaller lists
n = 20000
trees_95_chunks = [trees_95_tuples[i:i+n] for i in range(0,len(trees_95_tuples),n)]


# insert into database
for chunk in trees_95_chunks:
    add_tree_95 = ("""INSERT INTO trees_1995
               (tree_id, health, spc_latin, spc_common, address, zipcode, boroname, lat, lng)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""")

    cursor.executemany(add_tree_95, chunk)
    cnx.commit()
