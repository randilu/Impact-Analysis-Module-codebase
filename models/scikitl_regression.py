import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # Data visualisation libraries
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('seaborn')


def evaluate_news_analysis(company_name, impact_events_csv):
    fields = ['max_value', 'daily_news_vector_sum', 'close', 'impact']

    # fields = ['max_value', 'impact', 'daily_news_vector_sum']
    stock_trend_df = pd.read_csv(impact_events_csv, sep=',', usecols=fields)
    print(stock_trend_df)
    stock_trend_df.rename(columns={'max_value': 'max_trend'}, inplace=True)
    stock_trend_df.head()
    stock_trend_df.info()
    stock_trend_df.describe()
    sns.pairplot(stock_trend_df)
    plt.show()

    sns.distplot(stock_trend_df['daily_news_vector_sum'])
    plt.show()

    sns.distplot(stock_trend_df['max_trend'])
    plt.show()

    ax = sns.heatmap(stock_trend_df.corr(), cmap="YlGnBu")
    plt.show()
    corr = stock_trend_df.corr()
    corr = round(corr, 3)
    corr.to_csv(
        '/home/randilu/fyp_integration/Impact-Analysis-Module/evaluations/news_analysis_' + company_name + '_corr.csv')
    print(corr)

    X = stock_trend_df[['max_trend', 'daily_news_vector_sum', 'close']]
    y = stock_trend_df['impact']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

    lm = LinearRegression()
    lm.fit(X_train, y_train)

    predictions = lm.predict(X_test)
    print(lm.score(X, y))
    print('mean_absolute_error : ', mean_absolute_error(y_test, predictions))

    # plt.scatter(y_test, predictions)
    # plt.show()


# # run manually
# company = 'kelani_valley'
# impact_events_csv = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/final_output/kelani_valley_impact_events.csv'
# evaluate_news_analysis(company, impact_events_csv)
