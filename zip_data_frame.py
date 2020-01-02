import mysql_functions
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_zip_dataframe():
    data =  mysql_functions.get_zip_info()
    #retrieve data stored in MySQL

    df = pd.DataFrame(data, columns = ['zipcode', 'median_home_value', 'median_household_income', 'land_area_in_sqmi'])

    return df

print (create_zip_dataframe())
