from pandas import Series, DataFrame
from pytrends.request import TrendReq

import numpy as np
from sklearn import preprocessing

pytrends = TrendReq(hl='en-US', tz=330)

kw_list = ["Prime Minister"]

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
pytrend.build_payload(kw_list, cat=0, timeframe='2018-10-20 2018-11-20', geo='LK')

# Interest Over Time
interest_over_time_df = pytrend.interest_over_time()
# print(interest_over_time_df)

# df_new = interest_over_time_df[['date', 'Prime minister']]
# print(df_new)
x_array = np.array(interest_over_time_df.get(kw_list[0]))


normalized_X = preprocessing.normalize([x_array], 'max')
for value in normalized_X:
    y_array=value
    # for element in value:
    #     print(round(float(element), 2))
interest_over_time_df['Normalized_Trend'] = Series(y_array, index=interest_over_time_df.index)
json_data=interest_over_time_df.to_json('temp.json', orient='records', lines=True)

print(y_array)
print(interest_over_time_df)


trend_file1 = open("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/raw/trend_data/trend_file1.xlsx", "w")
trend_file1.write(str(interest_over_time_df))

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

x = interest_over_time_df.get(kw_list) #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df = DataFrame(x_scaled)
print(df)