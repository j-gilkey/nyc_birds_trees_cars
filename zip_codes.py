from uszipcode import SearchEngine
import mysql_functions
import tree_data_frame_creation as tree

search = SearchEngine(simple_zipcode=True)

def parse_zips():
    all_zip_codes = list(tree.create_tree_dataframe().zipcode.unique())

    #print(all_zip_codes)

    for zip in all_zip_codes:
        zip_data = search.by_zipcode(zip)
        #print(zip_data)
        if zip_data.median_home_value:
            zip_tuple = (int(zip), int(zip_data.median_home_value), int(zip_data.median_household_income), zip_data.land_area_in_sqmi)
            print(zip_tuple)
            mysql_functions.insert_zip(zip_tuple)


parse_zips()
