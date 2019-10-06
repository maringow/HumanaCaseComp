import pandas as pd
import scipy


# x_train = pd.read_csv('x_train.csv')
# y_train = pd.read_csv('y_train.csv')
# x_test = pd.read_csv('x_test.csv')
# y_test = pd.read_csv('y_test.csv')

# train-test split

x_train, x_test, y_train, y_test = train_test_split(df_outcomes_train, df_outcomes_test, test_size=.2, shuffle=True)

# x_train.to_csv('x_train.csv')
# x_test.to_csv('x_test.csv')
# y_train.to_csv('y_train.csv')
# y_test.to_csv('y_test.csv')
