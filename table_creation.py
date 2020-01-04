import mysql.connector
import config
from mysql.connector import errorcode

#set database name
DB_NAME = 'birds_trees_etc'

#create connection
cnx = mysql.connector .connect(
    host = config.host,
    user = config.user,
    passwd = config.password,
    database = DB_NAME,
    use_pure=True
)

#start cursor
cursor = cnx.cursor()


TABLES = {}
TABLES['birds'] = ("""
     CREATE TABLE birds (
      bird_obsv_id INT NOT NULL AUTO_INCREMENT ,
      speciesCode varchar(22) NOT NULL,
      comName varchar(22),
      sciName varchar(50),
      locId varchar(50),
      locName varchar(50),
      obsDt varchar(50),
      how_many int(22),
      lat decimal(10,8),
      lng decimal(10,8),
      PRIMARY KEY (bird_obsv_id)
    ) ENGINE=InnoDB""")

TABLES['trees_1995'] = (
"""CREATE TABLE trees_1995 (
    tree_id int NOT NULL,
    health varchar(10),
    spc_latin varchar(100),
    spc_common varchar(100),
    address varchar(150),
    zipcode int,
    boroname varchar(100),
    lat decimal(10,8),
    lng decimal(10,8),
    total_neighbors int,
    distinct_spc_neighbors int,
    same_spc_neighbors int,
    PRIMARY KEY (tree_id)
    );""")

TABLES['trees_2005'] = (
"""CREATE TABLE trees_2005 (
    tree_id int NOT NULL,
    health varchar(10),
    spc_latin varchar(100),
    spc_common varchar(100),
    address varchar(150),
    zipcode int,
    boroname varchar(100),
    lat decimal(10,8),
    lng decimal(10,8),
    total_neighbors int,
    distinct_spc_neighbors int,
    same_spc_neighbors int,
    PRIMARY KEY (tree_id)
    );""")

TABLES['trees_2015'] = (
"""CREATE TABLE trees_2015 (
    tree_id int NOT NULL,
    health varchar(10),
    spc_latin varchar(100),
    spc_common varchar(100),
    address varchar(150),
    zipcode int,
    boroname varchar(100),
    lat decimal(10,8),
    lng decimal(10,8),
    total_neighbors int,
    distinct_spc_neighbors int,
    same_spc_neighbors int,
    PRIMARY KEY (tree_id)
    );""")


TABLES['zip_demographics'] = (
"""CREATE TABLE zip_demographics(
    zip_code int NOT NULL,
    median_home_value int,
    median_household_income int,
    land_area_in_sqmi decimal(20,8),
    PRIMARY KEY (zip_code)
    );""")

#table creation function accepts a list and exectutes each element
def table_creation(table_list):
    for table_name in table_list:
        table_description = table_list[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

table_creation(TABLES)
