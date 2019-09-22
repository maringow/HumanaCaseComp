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

# build outcomes dataframe - at member level, to be populated with LTOT outcome
df_outcomes = pd.DataFrame(columns=['id', 'count_leadup_events', 'ltot_status'])
df_outcomes['id'] = df_raw['id'].unique()

df_outcomes['count_leadup_events'] = df_outcomes['id']\
    .map(df_raw[df_raw['Days'] < 0]['id'].value_counts())

df_outcomes['ltot_status'] = 0

df_outcomes.head(10)

# create dataframe of all opioid prescriptions
df_opioid = df_raw[df_raw['event_descr'] == 'RX Claim - Paid']
df_opioid = df_opioid[df_opioid['MME'].isnull() == False]
df_opioid = df_opioid.rename(columns={'id': 'member_id'})

df_opioid.head()

# select only members that total at least 163 days of opioids supplied
df_total_opioid_counts = df_raw[['id', 'PAY_DAY_SUPPLY_CNT']].groupby('id').sum()
possible_positives = df_total_opioid_counts[df_total_opioid_counts['PAY_DAY_SUPPLY_CNT'] >= 162].index

len(possible_positives)

# build shell dataframe of member id, day, coverage, and qualifying events for days 0 onward

day_range = range(-1300, 1101)
index = pd.MultiIndex.from_product([possible_positives, day_range], names = ['member_id', 'day'])
df_coverage = pd.DataFrame(index=index).reset_index()
df_coverage['covered'] = 0
df_coverage['qe'] = 0

df_coverage.head()

# distribute opioid pay day supply counts across df_coverage. Day prescribed is day 1

df_opioid = df_opioid[df_opioid['member_id'] == 'ID10013863216']  # test with 1 ID - remove later
df_opioid.head(50)

for i in df_opioid.index:
    day = df_opioid['Days'][i]
    member_id = df_opioid['member_id'][i]
    count = df_opioid['PAY_DAY_SUPPLY_CNT'][i]
    while count > 0:
        df_coverage[(df_coverage['day'] == day) & (df_coverage['member_id'] == member_id)]['covered'] = 1
        day += 1
        count = count - 1

df_coverage.head()


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