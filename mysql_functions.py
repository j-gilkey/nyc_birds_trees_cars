import mysql.connector
import config

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

def insert_bird(bird_tuple):
    add_bird = ("""INSERT INTO birds
               (speciesCode, comName, sciName, locId, locName, obsDt, how_many, lat, lng)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""")

    cursor.execute(add_bird, bird_tuple)
    cnx.commit()

def get_all_bird_obsv_id_and_lng_lat():
    get_all = ('''SELECT bird_obsv_id, lat, lng FROM birds''')
    cursor.execute(get_all)
    return cursor.fetchall()


def insert_tree(tree_tuples):
    add_tree = ("""INSERT INTO trees
               (tree_id, health, spc_latin, spc_common, address, zipcode, zip_city, borocode, boroname, lat, lng)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""")

    cursor.execute(add_tree, tree_tuples)
    cnx.commit()
