# importing prophet
from fbprophet import Prophet
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('seaborn')

# creating dataframe
file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/stock-data-companies/bogawanthalawa.csv'
df = pd.read_csv(file)
new_data = pd.DataFrame(index=range(0, len(df)), columns=['Date', 'Close'])

for i in range(0, len(df)):
    new_data['Date'][i] = df['date'][i]
    new_data['Close'][i] = df['close'][i]

new_data['Date'] = pd.to_datetime(new_data.Date, format='%Y-%m-%d')
new_data.index = new_data['Date']
# preparing data
new_data.rename(columns={'Close': 'y', 'Date': 'ds'}, inplace=True)

# # log transform for get non stationary points
# np.log(new_data['y'].astype(np.float64))
#
# new_data['y_orig'] = new_data['y']
# # new_data['y'] = np.log(new_data['y'])
# new_data['y'] = np.log(new_data['y'].astype(np.float64))


# train and validation
train = new_data[:1170]
# train = train[-500:]
valid = new_data[1170:]

print(train)
train['y_orig'] = train['y']
train['y'] = np.log(train['y'].astype(np.float64))


# fit the model
model = Prophet()
model.fit(train)

# predictions
close_prices = model.make_future_dataframe(periods=len(valid))
forecast = model.predict(close_prices)

forecast_valid = forecast['yhat'][1170:]

forecast_valid = np.exp(forecast_valid)

rms = np.sqrt(np.mean(np.power((np.array(valid['y']) - np.array(forecast_valid)), 2)))
print(rms)

# # plot
# valid['Predictions'] = 0
# valid['Predictions'] = forecast_valid.values
#
# plt.plot(train['y_orig'])
# plt.plot(valid[['y', 'Predictions']])
# plt.show()

# # performance metrics
# metric_df = forecast.set_index('ds')[['yhat']].join(new_data.set_index('ds').y).reset_index()
# print(metric_df.tail())
# metric_df.dropna(inplace=True)
# print(metric_df.tail())
# print('r2_score : ', r2_score(metric_df.y, metric_df.yhat))
# print('mean_squared_error : ', mean_squared_error(metric_df.y, metric_df.yhat))
# print('mean_absolute_error : ', mean_absolute_error(metric_df.y, metric_df.yhat))
