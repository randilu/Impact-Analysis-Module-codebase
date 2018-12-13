from pandas import Series, DataFrame
from pytrends.request import TrendReq

import numpy as np
import pandas as pd
from sklearn import preprocessing

pytrends = TrendReq(hl='en-US', tz=330)

kw_list = ["Storm", "mahinda", "Prime Minister", "ranil", "home"]

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
pytrend.build_payload(kw_list, cat=0, timeframe='2017-01-01 2017-12-31', geo='LK')

# Interest Over Time
interest_over_time_df = pytrend.interest_over_time()
print(interest_over_time_df)

'''
x_array = np.array(interest_over_time_df.get(kw_list[0]))
normalized_X = preprocessing.normalize([x_array], 'max')
for value in normalized_X:
    y_array = value
    for element in value:
        print(round(float(element), 2))
interest_over_time_df['Normalized_Trend'] = Series(y_array, index=interest_over_time_df.index)
json_data=interest_over_time_df.to_json('temp.json', orient='records', lines=True)
print(y_array)
print(interest_over_time_df)
trend_file1 = open("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/raw/trend_data/trend_file1.xlsx", "w")
trend_file1.write(str(interest_over_time_df))

'''

# Interest by Region
# interest_by_region_df = pytrend.interest_by_region()
# print(interest_by_region_df.head())
#
# # Related Queries, returns a dictionary of dataframes
# related_queries_dict = pytrend.related_queries()
# print(related_queries_dict)
#
#
# # Get Google Top Charts
# top_charts_df = pytrend.top_charts(cid='actors', date=201611)
# print(top_charts_df.head())
#
# # Get Google Keyword Suggestions
# suggestions_dict = pytrend.suggestions(keyword='pizza')
# print(suggestions_dict)

x = interest_over_time_df.get(kw_list)  # returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df = DataFrame(x_scaled)
rounded = df.round(2)
rounded.index = interest_over_time_df.index
df = interest_over_time_df.drop(columns=['isPartial'])
columns = pd.DataFrame(columns=df.columns)
rounded.columns = [columns]
print(rounded)
trend_file3 = rounded.to_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/raw/trend_data/trend_file3.csv", sep='\t',encoding='utf-8')
# trend_file2 = open("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/raw/trend_data/trend_file2.csv", "w")
# trend_file2.write(str(rounded))

stock_data_df=pd.read_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/interim/cse_data/CSE_market_indices_2017 - Sheet1.csv")
stock_data_df['date'] = pd.to_datetime(stock_data_df['date'], format="%Y/%m/%d")
stock_data_df=stock_data_df.set_index('date')

result = pd.concat([rounded, stock_data_df], axis=1, join_axes=[rounded.index])
print(stock_data_df)
print(result)
print(rounded.index)
print(stock_data_df.index)