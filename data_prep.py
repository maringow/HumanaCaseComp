import pandas as pd
import numpy as np

#####################################################################################
# DATA PREP
#####################################################################################

# set head() to show all columns and 20 rows
pd.set_option('display.max_columns', None)

# read in data
df_raw = pd.read_csv('C:\\Users\\mgow\\Documents\\Personal\\Humana Case Comp\\HMAHCC_COMP.csv')
print(df_raw.head(n=10))

df = pd.DataFrame(columns=['id', 'count_leadup_events', 'ltot_status'])
df['id'] = df_raw['id'].unique()

# count how many events each member had before Day 0
df['count_leadup_events'] = df['id'].map(df_raw[df_raw['Days'] < 0]['id'].value_counts())

# create temporary dataframe of 180-day opioid supply for LTOT calculation and merge into df
#TODO make this extensibly to 180-day rolling window
df_supply_first_180 = df_raw[(df_raw['Days'] >= 0) & (df_raw['Days'] < 180)][['id', 'PAY_DAY_SUPPLY_CNT']]\
    .groupby(['id']).sum()

df = df.merge(
    df_supply_first_180,
    on='id',
    how='left'
)

df = df.rename(columns={'PAY_DAY_SUPPLY_CNT': 'supply_first_180'})

# set LTOT status based on opioid supply count
df['ltot_status'] = df['supply_first_180'].apply(lambda x: 1 if x >= 162 else 0)

print(df.head(100))



#####################################################################################
# FEATURE ENGINEERING
#####################################################################################






#####################################################################################
# TRAIN-TEST SPLIT
#####################################################################################






#####################################################################################
# MODEL EVALUATION
#####################################################################################





#####################################################################################
# CROSS-VALIDATION
#####################################################################################




#####################################################################################
# RESULT OUTPUT
#####################################################################################