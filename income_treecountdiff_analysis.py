# import packages/modules
import mysql.connector
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
import tree_dataframe
import tree_data_frame_creation as dfcreate
import zip_data_frame as zipcreate

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


treedf = dfcreate.create_tree_dataframe_health()
zipdf = zipcreate.create_zip_dataframe()


pd.set_option('display.max_columns', 999)
pd.set_option('display.max_rows', 999)
df = pd.merge(treedf, zipdf, on='zipcode')
df = df.drop(columns=['median_home_value', 'land_area_in_sqmi'])

"""hypothesis: 1.) higher income areas will have more healthy trees; healthy over time
"""

avg_count = pd.DataFrame(df.groupby(['zipcode', 'median_household_income', 'healthy'])['tree_count'].mean())


totalcount = pd.DataFrame(df.groupby(['zipcode', 'median_household_income', 'healthy', 'year'])['tree_count'].mean())
totalcount = (totalcount.sort_values('median_household_income', ascending=False)).reset_index()
# print(totalcount.head())


df1 = totalcount.zipcode.value_counts().reset_index()
df2 = df1[df1['zipcode'] == 6]
df2.columns = ['zipcode', 'cnt_zips']
df3 = pd.merge(totalcount, df2, on='zipcode', how='inner')


totalcounts_6 = df3[df3['cnt_zips'] == 6]
total_counts_6 = totalcounts_6.sort_values(by=['median_household_income', 'year'], ascending=False)


total_counts_unhealthy = total_counts_6.drop(total_counts_6[total_counts_6.healthy == 1].index)
# print(total_counts_unhealthy)

concat_df = pd.DataFrame(columns=['index',  'zipcode',  'median_household_income',  'healthy',  'year' , 'tree_count', 'cnt_zips', 'tree_diff'])

incomes_list = list(total_counts_unhealthy.median_household_income.unique())

concat_df = pd.DataFrame(columns=['index',  'zipcode',  'median_household_income',  'healthy',  'year' , 'tree_count', 'cnt_zips', 'tree_diff'])
# print(incomes_list)
for income in incomes_list:
    income_count_list = ((total_counts_unhealthy[total_counts_unhealthy['median_household_income'] == income])).reset_index()
    tree_count_diff = ((income_count_list.tree_count.diff(periods=-1)).reset_index())
    tree_count_diff.columns = ['index2', 'tree_diff']
    income_count_diff = pd.concat([income_count_list, tree_count_diff], axis=1)
    income_count_diff = income_count_diff.drop(columns=['index2'])
    concat_df = pd.concat([concat_df, income_count_diff])
#     print(income_count_diff)

income_diff = concat_df.groupby(['zipcode', 'median_household_income'])['tree_diff'].sum().reset_index()
income_diff = income_diff.sort_values('median_household_income', ascending=False)
print(income_diff)


def scatter(df):
    fig = plt.figure()
    plt.style.use('seaborn')
    sns.set_palette('colorblind')
    ax = sns.scatterplot(x = 'year', y = 'tree_count', hue = 'median_household_income', data = df)
    plt.show()

# scatter(total_counts_unhealthy)

def hist_plot(df):
    fig = plt.figure()
    plt.style.use('seaborn')
    sns.set_palette('colorblind')
    hist_serial = sns.distplot(df['median_household_income'], kde = False)
    hist_serial.set_xlabel('Median Household Income')
    #hist_serial.set_xlabel('Trees per sq Mile')
    plt.show()

# hist_plot(total_counts_unhealthy)

def simple_box(df):
    fig = plt.figure()
    plt.style.use('seaborn')
    sns.set_palette('colorblind')
    ax = sns.boxplot(x= 'median_household_income', y = 'tree_count', data = df)

    #ax.set_ylabel('Median Home Value')
    ax.set_ylabel('Tree Count')
    ax.set_xlabel('Median Household Income')
    plt.show()

# simple_box(total_counts_unhealthy)

def anova_tree(df):
    anova_zip = ols('median_home_value~trees_per_sq_mile', data = df[['trees_per_sq_mile','median_home_value']].astype(float)).fit()
    anova_table = sm.stats.anova_lm(anova_zip, type=2)
    print(df.shape)
    print(anova_table)

#anova_tree(big_df)

def multicomp_income(df):
    mc = MultiComparison(df['median_household_income'], df['tree_count'])
    mc_results = mc.tukeyhsd()
    print(mc_results)

# multicomp_income(total_counts_unhealthy)
