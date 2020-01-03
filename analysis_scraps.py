import mysql_functions
import pandas as pd
import seaborn as sns
import tree_data_frame_creation
import zip_data_frame
from statsmodels.formula.api import ols
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison
from scipy.stats import ttest_ind
from scipy.stats import pearsonr
from scipy import stats
import random

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

tree_df = tree_data_frame_creation.create_distinct_tree_dataframe()
#print(tree_df)
tree_df = tree_df[tree_df['year'] == '2015']
#print(tree_df)
zip_df = zip_data_frame.create_zip_dataframe()

big_df = pd.merge(tree_df, zip_df, on = 'zipcode', how='inner')
big_df['trees_per_sq_mile'] = big_df['tree_count']/big_df['land_area_in_sqmi']
big_df['trees_per_sq_mile'] = big_df['trees_per_sq_mile'].astype(float)
#big_df['normalized'] =
big_df['median_home_value'] = big_df['median_home_value'].astype(float)

# df_man = big_df[big_df['boro'] == 'Manhattan']
# df_stat = big_df[big_df['boro'] == 'Staten Island']
# df_bron = big_df[big_df['boro'] == 'Bronx']
df_queen = big_df[big_df['boro'] == 'Queens']
# df_brook = big_df[big_df['boro'] == 'Brooklyn']
# boro_list = [df_man, df_stat, df_bron, df_queen, df_brook]
#print(list(big_df.boro.unique()))

#print(big_df)


def scatter(df):
    fig = plt.figure()
    plt.style.use('seaborn')
    sns.set_palette('colorblind')
    ax = sns.scatterplot(x = 'trees_per_sq_mile', y = 'median_home_value', hue = 'boro', data = df)
    plt.show()

#scatter(big_df)

def hist_plot(df):
    fig = plt.figure()
    plt.style.use('seaborn')
    sns.set_palette('colorblind')
    hist_serial = sns.distplot(df['median_home_value'], kde = False)
    hist_serial.set_xlabel('Median Home Value')
    #hist_serial.set_xlabel('Trees per sq Mile')
    plt.show()

#hist_plot(big_df)

def simple_box(df):
    fig = plt.figure()
    plt.style.use('seaborn')
    sns.set_palette('colorblind')
    ax = sns.boxplot(x= 'boro', y = 'trees_per_sq_mile', data = df)

    #ax.set_ylabel('Median Home Value')
    ax.set_ylabel('Trees per sq Mile')
    ax.set_xlabel('Borough')
    plt.show()

#simple_box(big_df)

def anova_tree(df):
    anova_zip = ols('median_home_value~trees_per_sq_mile', data = df[['trees_per_sq_mile','median_home_value']].astype(float)).fit()
    anova_table = sm.stats.anova_lm(anova_zip, type=2)
    print(df.shape)
    print(anova_table)

#anova_tree(big_df)

def multicomp_variable(df, basis):
    mc = MultiComparison(df[basis], df['test_or_control'])
    mc_results = mc.tukeyhsd()
    print(mc_results)


def pearsonr_by_boro(df):
    df_man = df[df['boro'] == 'Manhattan']
    df_stat = df[df['boro'] == 'Staten Island']
    df_bronx = df[df['boro'] == 'Bronx']
    df_queens = df[df['boro'] == 'Queens']
    df_brook = df[df['boro'] == 'Brooklyn']
    boro_list = [df_man, df_stat, df_bron, df_queen, df_brook]

    print(pearsonr(big_df['median_home_value'], big_df['trees_per_sq_mile']))

    for boros in boro_list:
        print(boros.boro.unique())
        print(pearsonr(boros['median_home_value'], boros['trees_per_sq_mile']))

#pearsonr_by_boro(big_df)

# def compare_zip_to_sample(zips, sample_size = 10, year = '2015', borough = 'any'):
#     table = 'trees_' + str(year)
#     zip_list = mysql_functions.get_zip_list(table, borough)
#     zip_samples = random.sample(zip_list, sample_size)
#     print(zip_samples)
#
#     control_df = big_df[big_df['zipcode'].isin(zip_samples)]
#     #print(control_df)
#     control_df['test_or_control'] = 'control'
#
#     test_df = big_df[big_df['zipcode'].isin(zips)]
#     test_df['test_or_control'] = 'test'
#
#     final_df = pd.concat([control_df, test_df])
#
#     return final_df

def compare_zip_to_pop(zips, df):
    df['test_or_control'] = 'control'
    df.loc[df.zipcode.isin(zips), 'test_or_control'] = 'test'
    return df

example_df = compare_zip_to_pop(['11001', '11363'], df_queen)
print(example_df)

multicomp_variable(example_df, 'median_home_value')


#print(compare_zip_to_sample(['11001', '11363'], 5))

#print(df_queen.sort_values(by=['median_household_income']))
