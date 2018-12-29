import pandas as pd
from pytrends.request import TrendReq
from src.data.fetch_trend_data_utils import normalize_trends, remove_weekends

pytrends = TrendReq(hl='en-US', tz=330)

# kw_list = [['Storm', 'mahinda', 'Prime Minister', 'ranil', 'home'], ['Toyota']]
kw_list = [['Tea'], ['gsp+'], ['floods']]
# kw_list = [['Storm']]


# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend1 = TrendReq()
pytrend2 = TrendReq()
# list which contains set of data frames each corresponding to a keyword
joined_trend_dfs_list = []
for i, sub_list in enumerate(kw_list, start=0):
    # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
    pytrend1.build_payload(sub_list, cat=0, timeframe='2017-01-01 2017-09-27', geo='LK')
    pytrend2.build_payload(sub_list, cat=0, timeframe='2017-09-27 2017-12-30', geo='LK')

    # Interest Over Time
    interest_over_time_df1 = pytrend1.interest_over_time()
    interest_over_time_df2 = pytrend2.interest_over_time()
    # print(interest_over_time_df1)
    # print(interest_over_time_df2)
    rounded_df1 = normalize_trends(interest_over_time_df1, sub_list)
    rounded_df2 = normalize_trends(interest_over_time_df2, sub_list)
    frames = [rounded_df1, rounded_df2]
    # joining the data frames and appending into above specified list
    joined_trend_dfs_list.append(pd.concat(frames))

# concatenating all the data frames to single data frame
combined_trend_data_df = pd.concat(joined_trend_dfs_list, axis=1, sort=False)
combined_trend_data_df['max_value'] = combined_trend_data_df.max(axis=1)
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
stock_data_df = pd.read_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/interim/cse_data/CSE_market_indices_2017 - Sheet1.csv",sep=None, thousands=',')
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
stock_trend_combined = result_df.to_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/interim/trend_data/stock_trend_combined.csv",sep='\t', encoding='utf-8', index=False)
formated_df = pd.read_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/interim/trend_data/stock_trend_combined.csv",sep='\t', encoding='utf-8')
formated_df.columns = formated_df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('\'', '').str.replace(',', '')
formated_df = formated_df.dropna()
print(formated_df)
formated_df.to_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/processed/trend_data/stock_trend_formated.csv",sep='\t', encoding='utf-8', index=False)
