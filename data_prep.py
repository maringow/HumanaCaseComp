import pandas as pd
import numpy as np
import math

#####################################################################################
# DATA PREP
#####################################################################################

# set head() to show all columns and 20 rows
pd.set_option('display.max_columns', None)

# read in data
df_raw = pd.read_csv('C:\\Users\\mgow\\Documents\\Personal\\Humana Case Comp\\HMAHCC_COMP.csv')
print(df_raw.head(n=10))

# build outcomes dataframe - at member level, to be populated with LTOT outcome
df_outcomes = pd.DataFrame(columns=['id', 'count_leadup_events', 'ltot_status'])
df_outcomes['id'] = df_raw['id'].unique()

df_outcomes['count_leadup_events'] = df_outcomes['id']\
    .map(df_raw[df_raw['Days'] < 0]['id'].value_counts())

df_outcomes['ltot_status'] = 0

print(df_outcomes.head(10))

# create dataframe of all opioid prescriptions
df_opioid = df_raw[(df_raw['event_descr'] == 'RX Claim - Paid') & (df_raw['MME'].isnull() == False)]
df_opioid = df_opioid.rename(columns={'id': 'member_id'})

print(df_opioid.head())

# select only members that total at least 163 days of opioids supplied
df_total_opioid_counts = df_raw[['id', 'PAY_DAY_SUPPLY_CNT']].groupby('id').sum()
possible_positives = df_total_opioid_counts[df_total_opioid_counts['PAY_DAY_SUPPLY_CNT'] >= 162].index

len(possible_positives)
possible_positives = possible_positives.sort_values()
possible_positives

# build shell dataframe of member id, day, coverage, and qualifying events for days 0 onward
day_range = range(-1300, 1101)
index = pd.MultiIndex.from_product([possible_positives, day_range], names = ['member_id', 'day'])
df_coverage = pd.DataFrame(index=index).reset_index()
df_coverage['covered'] = 0
df_coverage['qe'] = 0
df_coverage = df_coverage.merge(df_opioid[['member_id', 'Days', 'PAY_DAY_SUPPLY_CNT']], left_on=(['member_id', 'day']), \
                  right_on=(['member_id', 'Days']), how='left')

df_coverage = df_coverage.drop(columns=['Days'])
df_coverage = df_coverage.rename(columns={'PAY_DAY_SUPPLY_CNT': 'days_supply'})

# df_coverage = df_coverage[df_coverage['member_id'] == 'ID10013863216']  # for testing a single member
print(df_coverage[df_coverage['days_supply'].isnull() == False].head())

for g in df_coverage.sort_values(['member_id', 'day']).groupby('member_id').groups.values():
    supply = 0
    for i in g:
        dfi = df_coverage.loc[i]
        if not math.isnan(dfi.days_supply) and int(dfi.days_supply):
            supply += int(dfi.days_supply)
        if supply:
            df_coverage.loc[i, 'covered'] = 1
            supply -= 1

print(df_coverage[1300:1400])



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