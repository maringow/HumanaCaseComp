import pandas as pd
import numpy as np
import data_prep

#####################################################################################
# FEATURE ENGINEERING
#####################################################################################

df_features = pd.read_csv('df_outcomes.csv')
df_raw = pd.read_csv('C:\\Users\\mgow\\Documents\\Personal\\Humana Case Comp\\HMAHCC_COMP.csv')


# days before 0 - used to standardize
df_days_before_0 = df_raw[['id', 'Days']].groupby('id').min().reset_index()
df_days_before_0 = df_days_before_0.rename(columns={'Days': 'days_before_0'})
df_days_before_0['days_before_0'] = abs(df_days_before_0['days_before_0'])

df_outcomes = pd.read_csv('C:\\Users\\mgow\\Documents\\Personal\\Humana Case Comp\\df_outcomes.csv')
df_outcomes = df_outcomes.merge(df_days_before_0, how = 'left', left_on = 'member_id', right_on = 'id', right_index=False)
df_outcomes.drop(columns='id', inplace=True)

# Total number of different prescriptions that they’ve had prior to day 0 / days before 0
df_prescriptions = df_raw.loc[(df_raw.event_descr == 'RX Claim - Paid') & (df_raw.Days < 0)]
df_prescriptions.rename(columns={'id': 'member_id'}, inplace=True)

df_unique_prescriptions = df_prescriptions[['member_id', 'event_attr5']].groupby('member_id').nunique()
df_unique_prescriptions.drop(columns='member_id', inplace=True)
df_unique_prescriptions.rename(columns={'event_attr5': 'count_unique_scripts'}, inplace=True)

df_outcomes = df_outcomes.merge(df_unique_prescriptions, how = 'left', on = 'member_id', right_index=False)
df_outcomes.head()

# Supply sum of opioids before day 0 / number of days before 0

# Flag if they have taken Psych

# Flag if they have taken Pain

# Flag if they took opioids before day 0




