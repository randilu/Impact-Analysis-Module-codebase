import pandas as pd
import fbprophet as Prophet
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# to plot within notebook
import matplotlib.pyplot as plt
from sklearn.utils.testing import mock_mldata_urlopen

from stock_analysis.iam_util.iam_utils import calculate_impact, calculate_impact_modeled, get_impact_points

plt.rcParams['figure.figsize'] = (20, 10)
# plt.style.use('fivethirtyeight')
plt.style.use('ggplot')

# reading from csv
stock_df = pd.read_csv('/home/randilu/python_pojects/fyp/iam_model/data/stock_data/kelani_valley_2013_to_2018.csv',
                       sep='\,'
                       , encoding='utf-8', index_col='date', parse_dates=True)
print(stock_df.head())
df = stock_df.reset_index()
print(df.head())
df = df.rename(columns={'date': 'ds', 'close': 'y'})
print(df.head())
df.set_index('ds').y.plot()
plt.show()

#
# applying prophet model
#

model = Prophet.Prophet(changepoint_range=1, changepoint_prior_scale=0.05)
model.fit(df)

# Create future dataframe
future = model.make_future_dataframe(periods=90)
print(future.tail())

# Forecast for future dataframe
forecast = model.predict(future)
print(forecast.tail())
print('Forecast: \n', forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

model.plot(forecast)
model.plot_components(forecast)
plt.show()

viz_df = df.join(forecast[['yhat', 'yhat_lower', 'yhat_upper']], how='outer')
viz_df[['y', 'yhat']].plot()
plt.show()

new_df = calculate_impact_modeled(viz_df, 2)
new_df.rename(columns={'ds': 'date'}, inplace=True)
new_df = new_df[['date', 'impact']]
stock_df = pd.merge(stock_df, new_df, on=['date'], how='left')

#
# change point detection
#
changepoints = model.changepoints

cp_df = pd.DataFrame({'date': changepoints})
pd.to_datetime(cp_df['date'])
print(cp_df)
cp_with_impact = pd.merge(cp_df, stock_df, on=['date'], how='left')
print(cp_with_impact)
cp_with_impact = cp_with_impact[['date', 'impact']]
print(cp_with_impact)

#
# calculate the impact of each changepoint
#

cp_with_impact.to_csv('/home/randilu/python_pojects/fyp/iam_model/data/changepoints/modeled_changepoints.csv', sep='\t'
                      , encoding='utf-8', index=False)

impacts_df = stock_df
impacts_df.reset_index(drop=True, inplace=True)
impacts_df.set_index('date', inplace=True)
print(impacts_df)
impact_points_df = get_impact_points(stock_df)
impact_points_df.to_csv('/home/randilu/python_pojects/fyp/iam_model/data/changepoints/modeled_impactpoints.csv',
                        sep='\t'
                        , encoding='utf-8', index=False)

# figure = model.plot(forecast)

deltas = model.params['delta'].mean(0)
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111)
ax.bar(range(len(deltas)), deltas)
ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)
ax.set_ylabel('Rate change')
ax.set_xlabel('Potential changepoint')
fig.tight_layout()
plt.show()

# Create dataframe of only changepoints
change_indices = []
for changepoint in (changepoints):
    change_indices.append(df[df['ds'] == changepoint.date()].index[0])

c_data = df.loc[change_indices, :]
deltas = model.params['delta'][0]

c_data['delta'] = deltas
c_data['abs_delta'] = abs(c_data['delta'])

# Sort the values by maximum change
c_data = c_data.sort_values(by='abs_delta', ascending=False)

# Limit to 20 largest changepoints
c_data = c_data[:20]
c_data = c_data.sort_values(by='ds', ascending=False)
print(c_data)
print(stock_df)

# Separate into negative and positive changepoints
cpos_data = c_data[c_data['delta'] > 0]
cneg_data = c_data[c_data['delta'] < 0]

# Changepoints and data
# print('\nChangepoints sorted by slope rate of change (2nd derivative):\n')
dataframe = c_data.ix[:, ['ds', 'delta']][:30]
# dataframe.to_csv('/home/randilu/python_pojects/stock-analysis/data/predictions/changepoins_stocker.csv', sep='\t',
#                  encoding='utf-8', index=True)

# Set up line plot
plt.plot(df['ds'], df['y'], 'ko', ms=4, label='Stock Price')
plt.plot(forecast['ds'], forecast['yhat'], color='navy', linewidth=2.0, label='Modeled')

# Changepoints as vertical lines
plt.vlines(cpos_data['ds'].dt.to_pydatetime(), ymin=min(df['y']), ymax=max(df['y']),
           linestyles='dashed', color='r',
           linewidth=1.2, label='Negative Changepoints')

plt.vlines(cneg_data['ds'].dt.to_pydatetime(), ymin=min(df['y']), ymax=max(df['y']),
           linestyles='dashed', color='darkgreen',
           linewidth=1.2, label='Positive Changepoints')

plt.legend(prop={'size': 10})
plt.xlabel('Date')
plt.ylabel('Price (Rs)')
plt.title('Stock Price with Changepoints')
plt.show()

# performance metrics
metric_df = forecast.set_index('ds')[['yhat']].join(df.set_index('ds').y).reset_index()
print(metric_df.tail())
metric_df.dropna(inplace=True)
print(metric_df.tail())
print('r2_score : ', r2_score(metric_df.y, metric_df.yhat))
print('mean_squared_error : ', mean_squared_error(metric_df.y, metric_df.yhat))
print('mean_absolute_error : ', mean_absolute_error(metric_df.y, metric_df.yhat))
