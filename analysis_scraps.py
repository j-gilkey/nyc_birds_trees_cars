import mysql_functions
import pandas as pd
import seaborn as sns
import tree_data_frame_creation
import zip_data_frame
from statsmodels.formula.api import ols
import statsmodels.api as sm
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

tree_df = tree_data_frame_creation.create_distinct_tree_dataframe()
#print(tree_df)
tree_df = tree_df[tree_df['year'] == '2015']
#print(tree_df)
zip_df = zip_data_frame.create_zip_dataframe()

big_df = pd.merge(tree_df, zip_df, on = 'zipcode', how='inner')
big_df['trees_per_sq_mile'] = big_df['tree_count']/big_df['land_area_in_sqmi']

print(big_df)


def scatter(df):
    fig = plt.figure()
    plt.style.use('seaborn')
    sns.set_palette('colorblind')
    ax = sns.scatterplot(x = 'trees_per_sq_mile', y = 'median_home_value', hue = 'boro', data = df)
    plt.show()

#scatter(big_df)

def anova_tree(df):
    anova_zip = ols('trees_per_sq_mile~median_home_value', data = df[['trees_per_sq_mile','median_home_value']].astype(float)).fit()
    print(anova_zip.summary())

anova_tree(big_df)
