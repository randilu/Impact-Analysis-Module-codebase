import pandas as pd
import fbprophet as Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics

import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# to plot within notebook
import matplotlib.pyplot as plt
from sklearn.utils.testing import mock_mldata_urlopen

# from iam_util.iam_utils import calculate_impact

plt.rcParams['figure.figsize'] = (20, 10)
# plt.style.use('fivethirtyeight')
plt.style.use('ggplot')

# reading from csv
company_name = 'namunukula'
file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/stock-data-companies/namunukula.csv'
stock_df = pd.read_csv(file, sep=',', encoding='utf-8', index_col='date', parse_dates=True)
print(stock_df.head())
df = stock_df.reset_index()
print(df.head())
df = df.rename(columns={'date': 'ds', 'close': 'y'})
print(df.head())
df.set_index('ds').y.plot()
plt.show()

# # log transform for get non stationary points
# df['y_orig'] = df['y']
# df['y'] = np.log(df['y'])

#
# applying prophet model
#

model = Prophet.Prophet(changepoint_range=1, changepoint_prior_scale=0.05)
# model = Prophet.Prophet()
model.fit(df)

# # Create future dataframe
# future = model.make_future_dataframe(periods=90)
# print(future.tail())

df_cv = cross_validation(model, initial='730 days', period='90 days', horizon='180 days')
print(df_cv.head())

# from fbprophet.diagnostics import performance_metrics
df_p = performance_metrics(df_cv)
print(df_p.head())
df_p.to_csv('/home/randilu/fyp_integration/Impact-Analysis-Module/stock_analysis/models/evaluations' + company_name + '_evaluation.csv', sep=',',
            encoding='utf-8', index=False)

from fbprophet.plot import plot_cross_validation_metric
fig = plot_cross_validation_metric(df_cv, metric='mape')
plt.show()

fig2 = plot_cross_validation_metric(df_cv, metric='mae')
plt.show()

fig3 = plot_cross_validation_metric(df_cv, metric='rmse')
plt.show()

