import pandas as pd
import scipy
from sklearn.model_selection import train_test_split


pd.set_option('display.max_columns', None)
df = pd.read_csv('df_outcomes_features.csv')

df.drop(columns=['Unnamed: 0', 'index', 'X'], inplace=True)
df.set_index('member_id', inplace=True)

df_x = df.drop(columns='ltot_status')
print(df_x.head())
df_y = df['ltot_status']
print(df_y.head())

# train-test split

x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=.2, shuffle=True)


