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

# make API call for tree data
client = Socrata("data.cityofnewyork.us", 'tree_key')
client = Socrata('data.cityofnewyork.us',
                  config.tree_token,
                  username=config.od_user,
                  password=config.od_pw)
results = client.get("5rq2-4hqu", limit=690000)
# convert to pandas DataFrame
tree_data_total = pd.DataFrame.from_records(results)

# print(tree_data_total)


# select all rows and only the columns wanted
tree_data = pd.DataFrame(tree_data_total.loc[:, ['tree_id', 'health', 'spc_latin', 'spc_common', 'address', 'zipcode', 'zip_city', 'borocode', 'boroname', 'latitude', 'longitude']])

# parse tree data into tuples to insert into database
tree_tuples = list(tree_data.itertuples(index=False, name=None))
