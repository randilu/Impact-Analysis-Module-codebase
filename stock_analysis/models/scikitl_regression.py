import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # Data visualisation libraries
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

plt.rcParams['figure.figsize'] = (20, 10)
# plt.style.use('fivethirtyeight')
plt.style.use('seaborn')

fields = ['max_value', 'daily_news_vector_sum', 'high', 'low', 'close', 'open', 'trades', 'shares',
          'turnover', 'isImpacted', 'impact']
stock_trend_df = pd.read_csv(
    '/home/randilu/python_pojects/fyp/iam_model/data/processed/kv_plus_plantations_numeric.csv', usecols=fields)
stock_trend_df.rename(columns={'isImpacted': 'impact_score'}, inplace=True)
stock_trend_df.head()
stock_trend_df.info()
stock_trend_df.describe()
stock_trend_df.columns
stock_trend_df
sns.pairplot(stock_trend_df)
plt.show()

sns.distplot(stock_trend_df['daily_news_vector_sum'])
plt.show()

sns.distplot(stock_trend_df['max_value'])
plt.show()

ax = sns.heatmap(stock_trend_df.corr(), cmap="YlGnBu")
plt.show()
corr = stock_trend_df.corr()
corr = round(corr, 3)
corr.to_csv('/home/randilu/python_pojects/fyp/iam_model/data/results/scikit-results/corr.csv')
print(corr)

X = stock_trend_df[['max_value', 'daily_news_vector_sum']]
y = stock_trend_df['impact']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

lm = LinearRegression()
lm.fit(X_train, y_train)

predictions = lm.predict(X_test)
print(lm.score(X, y))

plt.scatter(y_test, predictions)
plt.show()
