from pandas import Series
import pandas as pd
from matplotlib import pyplot as plt
import datetime as dt

plt.rcParams['figure.figsize'] = (20, 10)
# plt.style.use('ggplot')
plt.style.use('fivethirtyeight')

file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/stock-data-plantations/kelani_valley_2013_to_2018.csv'
stock_df = pd.read_csv(file, sep='\,', encoding='utf-8', index_col='date', parse_dates=True)
# stock_df['date'] = pd.to_datetime(stock_df['date'], format="%Y/%m/%d")

stock_df['close'].plot()
plt.show()

series = stock_df['close']
# Tail-rolling average transform
rolling = series.rolling(window=4)
rolling_mean = rolling.mean()
stock_df['moving_avg'] = rolling_mean
stock_df['impact'] = round(((series - rolling_mean) / rolling_mean) * 100, 4)
# print(stock_df.tail())

impacts = stock_df[['impact']]
impacts['abs_impact'] = abs(impacts['impact'])
impacts = impacts.sort_values(by='abs_impact', ascending=False)
# print(impacts)

# Limit to 50 largest impactpoints
impacts = impacts[:50]
impacts.sort_index(inplace=True, ascending=False)
print(impacts)

# Converting the index as date
impacts.index = pd.to_datetime(impacts.index)
print(impacts.index.dtype)
impacts.reset_index(level=0, inplace=True)
print(impacts)

cp_df = impacts[['date', 'impact']]
print(cp_df)
# cp_df = pd.DataFrame({'date': impacts['date', 'impact']})
cp_df.to_csv('/home/randilu/fyp_integration/Impact-Analysis-Module/stock_analysis/data/changepoints/impactpoints.csv',
             sep='\t'
             , encoding='utf-8', index=False)

# Separate into negative and positive impactpoints
impos_data = impacts[impacts['impact'] > 0]
imneg_data = impacts[impacts['impact'] < 0]

series.plot(color='#1e8f90', label='Closing Stock Price')
rolling_mean.plot(color='black', label='Moving Average')
# plt.show()

# Changepoints as vertical lines
plt.vlines(imneg_data['date'].values, ymin=min(stock_df['close']), ymax=max(stock_df['close']),
           linestyles='dashed', color='#fe0707',
           linewidth=1.1, label='Negative Changepoints')

plt.vlines(impos_data['date'].values, ymin=min(stock_df['close']), ymax=max(stock_df['close']),
           linestyles='dashed', color='#261c76',
           linewidth=1.1, label='Positive Changepoints')

plt.legend(prop={'size': 10})
plt.xlabel('Date')
plt.ylabel('Price (Rs)')
plt.title('Stock Price with impact points')
plt.show()

# print standard deviation of close value
# print(Series.std(series))
