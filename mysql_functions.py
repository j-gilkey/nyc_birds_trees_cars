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


def insert_tree_1995(tree_tuples):
    add_tree = ("""INSERT INTO trees_1995
               (tree_id, health, spc_latin, spc_common, address, zipcode, boroname, lat, lng)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""")

    cursor.execute(add_tree, tree_tuples)
    cnx.commit()


def insert_tree_2005(tree_tuples):
    add_tree = ("""INSERT INTO trees_2005
               (tree_id, health, spc_latin, spc_common, address, zipcode, boroname, lat, lng)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""")

    cursor.execute(add_tree, tree_tuples)
    cnx.commit()

def insert_tree_2015(tree_tuples):
    add_tree = ("""INSERT INTO trees_2015
               (tree_id, health, spc_latin, spc_common, address, zipcode, boroname, lat, lng)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""")

    cursor.execute(add_tree, tree_tuples)
    cnx.commit()

def insert_zip(zip_tuple):
    add_zip = ("""INSERT INTO zip_demographics
               (zip_code, median_home_value, median_household_income, land_area_in_sqmi)
               VALUES (%s, %s, %s, %s);""")

    cursor.execute(add_zip, zip_tuple)
    cnx.commit()

def get_zip_info():

    get_zip  = ('(SELECT * FROM zip_demographics)')

    cursor.execute(get_zip)
    return cursor.fetchall()

def get_all_trees_agg():

    get_tree = ('''(SELECT spc_latin
                    		,zipcode
                    		,boroname
                    		,health
                            ,'1995' AS year
                    		,count(tree_id)
                    FROM trees_1995
                    GROUP BY spc_latin
                    		,zipcode
                    		,boroname
                    		,health
                    )

                    UNION ALL

                    (SELECT spc_latin
                    		,zipcode
                    		,boroname
                    		,health
                            ,'2005' AS year
                    		,count(tree_id)
                    FROM trees_2005
                    GROUP BY spc_latin
                    		,zipcode
                    		,boroname
                    		,health
                    )

                    UNION ALL

                    (SELECT spc_latin
                    		,zipcode
                    		,boroname
                    		,health
                            ,'2015' AS year
                    		,count(tree_id)
                    FROM trees_2015
                    GROUP BY spc_latin
                    		,zipcode
                    		,boroname
                    		,health
                    )''')

    cursor.execute(get_tree)
    return cursor.fetchall()
