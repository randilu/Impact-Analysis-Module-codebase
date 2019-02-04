import pandas as pd
from pytrends.request import TrendReq
from src.data.fetch_trend_data_utils import normalize_trends, remove_weekends, add_impact

pytrends = TrendReq(hl='en-US', tz=330)

# kw_list = [['Storm', 'mahinda', 'Prime Minister', 'ranil', 'home'], ['Toyota']]
kw_list = [['pest'], ['floods']]
# kw_list = [['Tea']]

# kw_list = [['Storm']]


# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend1 = TrendReq()
pytrend2 = TrendReq()
pytrend3 = TrendReq()
pytrend4 = TrendReq()
pytrend5 = TrendReq()
pytrend6 = TrendReq()
pytrend7 = TrendReq()
pytrend8 = TrendReq()
pytrend9 = TrendReq()
pytrend10 = TrendReq()
# list which contains set of data frames each corresponding to a keyword
joined_trend_dfs_list = []
for i, sub_list in enumerate(kw_list, start=0):
    # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
    pytrend1.build_payload(sub_list, cat=0, timeframe='2013-01-01 2013-09-27', geo='LK')
    pytrend2.build_payload(sub_list, cat=0, timeframe='2013-09-28 2013-12-30', geo='LK')
    pytrend3.build_payload(sub_list, cat=0, timeframe='2014-01-01 2014-09-27', geo='LK')
    pytrend4.build_payload(sub_list, cat=0, timeframe='2014-09-28 2014-12-30', geo='LK')
    pytrend5.build_payload(sub_list, cat=0, timeframe='2015-01-01 2015-09-27', geo='LK')
    pytrend6.build_payload(sub_list, cat=0, timeframe='2015-09-28 2015-12-30', geo='LK')
    pytrend7.build_payload(sub_list, cat=0, timeframe='2016-01-01 2016-06-30', geo='LK')
    pytrend8.build_payload(sub_list, cat=0, timeframe='2016-07-01 2016-12-30', geo='LK')
    pytrend9.build_payload(sub_list, cat=0, timeframe='2017-01-01 2017-09-27', geo='LK')
    pytrend10.build_payload(sub_list, cat=0, timeframe='2017-09-28 2017-12-30', geo='LK')

    # Interest Over Time
    interest_over_time_df1 = pytrend1.interest_over_time()
    interest_over_time_df2 = pytrend2.interest_over_time()
    interest_over_time_df3 = pytrend3.interest_over_time()
    interest_over_time_df4 = pytrend4.interest_over_time()
    interest_over_time_df5 = pytrend5.interest_over_time()
    interest_over_time_df6 = pytrend6.interest_over_time()
    interest_over_time_df7 = pytrend7.interest_over_time()
    interest_over_time_df8 = pytrend8.interest_over_time()
    interest_over_time_df9 = pytrend9.interest_over_time()
    interest_over_time_df10 = pytrend10.interest_over_time()
    # print(interest_over_time_df1)
    # print(interest_over_time_df2)
    rounded_df1 = normalize_trends(interest_over_time_df1, sub_list)
    rounded_df2 = normalize_trends(interest_over_time_df2, sub_list)
    rounded_df3 = normalize_trends(interest_over_time_df3, sub_list)
    rounded_df4 = normalize_trends(interest_over_time_df4, sub_list)
    rounded_df5 = normalize_trends(interest_over_time_df5, sub_list)
    rounded_df6 = normalize_trends(interest_over_time_df6, sub_list)
    rounded_df7 = normalize_trends(interest_over_time_df7, sub_list)
    rounded_df8 = normalize_trends(interest_over_time_df8, sub_list)
    rounded_df9 = normalize_trends(interest_over_time_df9, sub_list)
    rounded_df10 = normalize_trends(interest_over_time_df10, sub_list)
    frames = [rounded_df1, rounded_df2, rounded_df3, rounded_df4, rounded_df5, rounded_df6, rounded_df7, rounded_df8, rounded_df9, rounded_df10]
    # joining the data frames and appending into above specified list
    joined_trend_dfs_list.append(pd.concat(frames))

# concatenating all the data frames to single data frame
combined_trend_data_df = pd.concat(joined_trend_dfs_list, axis=1, sort=False)
combined_trend_data_df['max_value'] = combined_trend_data_df.max(axis=1)
combined_trend_data_df.to_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/interim/trend_data/trend_only_combined_plantations.csv",sep='\t', encoding='utf-8', index=True)


# combined_trend_data_df = combined_trend_data_df.loc[~combined_trend_data_df.index.duplicated(keep='first')]

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

# Loading local stock data
stock_data_df = pd.read_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/interim/cse_data/cse_market indices_from_2013_to_2017.csv", sep=None, thousands=',')
stock_data_df['date'] = pd.to_datetime(stock_data_df['date'], format="%Y/%m/%d")
stock_data_df = stock_data_df.set_index('date')
# stock_data_df['new_col'] = (stock_data_df['Services'].pct_change()*100).round(2)
stock_data_pct_change_df = (stock_data_df.pct_change()*100).round(2)

#
# combining trend data and stock data
#
result_df = pd.concat([combined_trend_data_df, stock_data_df, stock_data_pct_change_df], axis=1, sort=False)
result_df.reset_index(inplace=True)
result_df.set_index('date', drop=False, inplace=True)
result_df = remove_weekends(result_df)
stock_trend_combined = result_df.to_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/interim/trend_data/stock_trend_combined_plantations.csv",sep='\t', encoding='utf-8', index=False)
formated_df = pd.read_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/interim/trend_data/stock_trend_combined_plantations.csv",sep='\t', encoding='utf-8')
formated_df.columns = formated_df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('\'', '').str.replace(',', '').str.replace('.', '_')
formated_df = formated_df.dropna()
add_impact(formated_df)
print(formated_df)
formated_df.to_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/processed/trend_data/stock_trend_formated_plantations_from_2013_to_2017.csv",sep='\t', encoding='utf-8', index=False)
