import pandas as pd
import numpy as np
import data_prep
from sklearn.model_selection import train_test_split

#####################################################################################
# FEATURE ENGINEERING
#####################################################################################

# read in data
df_outcomes = pd.read_csv('df_outcomes.csv')
df_raw = pd.read_csv('C:\\Users\\mgow\\Documents\\Personal\\Humana Case Comp\\HMAHCC_COMP.csv')


# days before 0 - used to standardize
'''
QUERY FOR TESTING:

select id, count(distinct event_attr5), min(Days) from comp
where event_descr = 'RX Claim - Paid'
and Days < 0
group by id
order by count(distinct event_attr5) desc
'''

df_days_before_0 = df_raw[['id', 'Days']].groupby('id').min().reset_index()
df_days_before_0 = df_days_before_0.rename(columns={'Days': 'days_before_0'})
df_days_before_0['days_before_0'] = abs(df_days_before_0['days_before_0'])

df_outcomes = df_outcomes.merge(df_days_before_0, how = 'left', left_on = 'member_id', right_on = 'id', right_index=False)
df_outcomes.drop(columns='id', inplace=True)

# Total number of different prescriptions that they’ve had prior to day 0 / days before 0
df_prescriptions = df_raw.loc[(df_raw.event_descr == 'RX Claim - Paid') & (df_raw.Days < 0)]
df_prescriptions.rename(columns={'id': 'member_id'}, inplace=True)

df_unique_prescriptions = df_prescriptions[['member_id', 'event_attr5']].groupby('member_id').nunique()
df_unique_prescriptions.drop(columns='member_id', inplace=True)
df_unique_prescriptions.rename(columns={'event_attr5': 'count_unique_scripts'}, inplace=True)

df_outcomes = df_outcomes.merge(df_unique_prescriptions, how = 'left', on = 'member_id', right_index=False)

df_outcomes['count_unique_scripts_std'] = df_outcomes['count_unique_scripts'] / df_outcomes['days_before_0']

# Supply sum of opioids before day 0 / number of days before 0

'''
QUERY FOR TESTING:

select id, sum(cast(pay_day_supply_cnt as int)) from comp
where event_descr = 'RX Claim - Paid'
and MME is not null
and Days < 0
group by id
'''

df_opioid_prescriptions = df_raw.loc[(df_raw.event_descr == 'RX Claim - Paid') & (df_raw.Days < 0) & (df_raw.MME.isnull() == False)]
df_opioid_prescriptions.rename(columns={'id': 'member_id'}, inplace=True)

df_opioid_sum = df_prescriptions[['member_id', 'PAY_DAY_SUPPLY_CNT']].groupby('member_id').sum().reset_index()
df_opioid_sum.rename(columns={'PAY_DAY_SUPPLY_CNT': 'sum_prior_opioids'}, inplace=True)

df_outcomes = df_outcomes.merge(df_opioid_sum, how = 'left', on = 'member_id', right_index=False)
df_outcomes['sum_prior_opioids_std'] = df_outcomes['sum_prior_opioids'] / df_outcomes['days_before_0']

# Flag if they took opioids before day 0
df_outcomes['prior_opioids_flag'] = df_outcomes['sum_prior_opioids'].apply(lambda x: 1 if x > 0 else 0)


# flag if member has had a prior psych prescription

df_psych_prescriptions = df_raw.loc[(df_raw.event_descr == 'RX Claim - Paid') & (df_raw.Days < 0) & (df_raw.event_attr6.str.contains('PSYCH'))]
df_psych_prescriptions.rename(columns={'id': 'member_id'}, inplace=True)

prior_psych_members = df_psych_prescriptions['member_id'].unique()

df_outcomes['prior_psych_flag'] = df_outcomes['member_id'].apply(lambda x: 1 if x in prior_psych_members else 0)


# flag if member has had a prior pain prescription

df_pain_prescriptions = df_raw.loc[(df_raw.event_descr == 'RX Claim - Paid') & (df_raw.Days < 0) & (df_raw.event_attr6 == 'PAIN')]
df_pain_prescriptions.rename(columns={'id': 'member_id'}, inplace=True)

prior_pain_members = df_pain_prescriptions['member_id'].unique()

df_outcomes['prior_pain_flag'] = df_outcomes['member_id'].apply(lambda x: 1 if x in prior_pain_members else 0)

# check output
df_outcomes_features = df_outcomes.reset_index()
print(df_outcomes_features)
df_outcomes_features.to_csv('df_outcomes_features.csv')

#df_outcomes_test = df_outcomes[['ltot_status']]















