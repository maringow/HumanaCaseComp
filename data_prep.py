import pandas as pd
import numpy as np
import math

#####################################################################################
# CALCULATE OUTCOMES
#####################################################################################

# set head() to show all columns and 20 rows
pd.set_option('display.max_columns', None)

# read in data
df_raw = pd.read_csv('C:\\Users\\mgow\\Documents\\Personal\\Humana Case Comp\\HMAHCC_COMP.csv')
print(df_raw.head(n=10))


def build_outcomes_df(df_raw):

    # build outcomes dataframe - at member level, to be populated with LTOT outcome

    df_outcomes = pd.DataFrame(columns=['member_id', 'count_leadup_events', 'ltot_status'])
    df_outcomes['member_id'] = df_raw['id'].unique()

    df_outcomes['count_leadup_events'] = df_outcomes['member_id']\
        .map(df_raw[df_raw['Days'] < 0]['id'].value_counts())

    df_outcomes['ltot_status'] = 0

    df_outcomes.head(10)

    # create dataframe of all opioid prescriptions
    df_opioid = df_raw[(df_raw['event_descr'] == 'RX Claim - Paid') & (df_raw['MME'].isnull() == False)]
    df_opioid = df_opioid.rename(columns={'id': 'member_id'})
    df_opioid = df_opioid.reset_index(drop=True)

    # deduplicate by member and day - take max supply count if multiple scripts issued
    # create df of max counts by member & day
    df_max = df_opioid[['member_id', 'Days', 'PAY_DAY_SUPPLY_CNT']].groupby(['member_id', 'Days']).max(axis=1)
    df_max = df_max.rename(columns={'PAY_DAY_SUPPLY_CNT': 'max_supply_cnt'})
    df_max = df_max.reset_index()
    df_max.head()

    # merge this into df_opioid, and drop duplicates
    df_opioid = df_opioid.merge(df_max, how='left', on=['member_id', 'Days'])
    df_opioid.drop_duplicates(subset=('member_id', 'Days'), inplace=True)
    #df_opioid.to_csv('C:\\Users\\mgow\\Documents\\Personal\\Humana Case Comp\\check_max.csv')

    df_opioid.head(100)

    # select only members that total at least 163 days of opioids supplied
    df_total_opioid_counts = df_raw[['id', 'PAY_DAY_SUPPLY_CNT']].groupby('id').sum()
    possible_positives = df_total_opioid_counts[df_total_opioid_counts['PAY_DAY_SUPPLY_CNT'] > 162].index

    possible_positives = possible_positives.sort_values()
    possible_positives = possible_positives.tolist()

    # loops through members and identifies ltot status between Day 1 and Day 180

    n = 1

    for member in possible_positives:
        print(n)
        n += 1

        # get opioid events for days 1-180 and build df
        df_member = df_opioid.loc[(df_opioid.member_id == member) &
                                  (df_opioid.Days.between(0, 180)),
                                  ['Days', 'max_supply_cnt']]
        df_member = df_member.reset_index(drop=True)
        # print("All of member's opioid events: \n", df_member)

        # create shell of df_coverage - 1 record per day for 180 days after QE
        df_coverage = pd.DataFrame({'day': range(0, 181), 'covered': 0})

        # for each record in df_ltot_range, distribute across df_coverage
        for index, row in df_member.iterrows():
            # print(row)
            day = row['Days']
            days_supply = row['max_supply_cnt']
            rowshift = 0

            while days_supply > 0:
                df_coverage.loc[df_coverage.day == day + rowshift, 'covered'] = 1
                days_supply -= 1
                rowshift += 1

            # print('df_coverage: \n', df_coverage)

        # sum up df_coverage to see if it's LTOT; if it is, save result to df_outcomes and break
        # print('Total sum of covered days for this QE: \n', df_coverage['covered'].sum())
        if df_coverage['covered'].sum() > 162:
            df_outcomes.loc[df_outcomes.member_id == member, 'ltot_status'] = 1

    print(df_outcomes)

    # df_outcomes.to_csv('C:\\Users\\mgow\\Documents\\Personal\\Humana Case Comp\\df_outcomes.csv')



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