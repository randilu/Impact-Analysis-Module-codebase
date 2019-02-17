import pandas as pd
from pytrends.request import TrendReq

# from src.data.fetch_kw_from_csv_no_duplicates import kw_sent_list
# from src.data.fetch_kw_from_csv import kw_sent_list
# from src.data.fetch_kw_format2 import kw_sent_list
# from data.external.kw_list import new_list
from src.data.event_data.fetch_kw_format_dup_from_json import kw_sent_list
from src.data.fetch_trend_data_utils import normalize_trends, remove_weekends, add_impact, add_impact_from_changepoints, \
    split_sublist, create_news_vector, add_max_value, display_max_cols, calculate_impact, rename_duplicate_max_values, \
    create_date_range

display_max_cols(30)

pytrends = TrendReq(hl='en-US', tz=330)

kw_list = kw_sent_list
print(kw_sent_list)

# kw_list = [['Storm', 'mahinda', 'Prime Minister', 'ranil', 'home'], ['Toyota']]
# kw_list = [['Tea'], ['gsp+'], ['floods'], ['Prime Minister'], ['Ceylon Tea']]
# kw_list = [[0, '2017-12-15', 'tea', '-1'], [1, '2017-01-15', 'floods', '-1']]

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend1 = TrendReq()
# list which contains set of data frames each corresponding to a keyword
joined_trend_dfs_list = []
for i, sub_list in enumerate(kw_list, start=0):
    event_no, date, sub_list, sentiment = split_sublist(sub_list)
    int_sentiment = int(sentiment)
    sub_list = [sub_list]
    print(sub_list)
    start_date, end_date = create_date_range(date, 14, 14)
    # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
    pytrend1.build_payload(sub_list, cat=0, timeframe=start_date + " " + end_date, geo='LK')

    # Interest Over Time
    interest_over_time_df1 = pytrend1.interest_over_time()
    if interest_over_time_df1.empty:
        continue
    # print(interest_over_time_df1)
    # print(interest_over_time_df2)
    rounded_df1 = normalize_trends(interest_over_time_df1, sub_list)
    rounded_df1 *= int_sentiment
    rounded_df1 = rounded_df1.add_suffix('_' + str(event_no))
    frames = [rounded_df1]
    # joining the data frames and appending into above specified list
    joined_trend_dfs_list.append(pd.concat(frames))

# concatenating all the data frames to single data frame
combined_trend_data_df = pd.concat(joined_trend_dfs_list, axis=1, sort=False)
print(combined_trend_data_df.head())
add_max_value(combined_trend_data_df)
combined_trend_data_df['kw_max'] = combined_trend_data_df.apply(lambda x: x.abs().argmax(), axis=1)
combined_trend_data_df['daily_news_vector_sum'] = create_news_vector(combined_trend_data_df)
combined_trend_data_df.fillna(0, inplace=True)
print(combined_trend_data_df.head())

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
stock_data_df = pd.read_csv(
    "/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/stock-data-plantations/kelani_valley_2013_to_2018.csv",
    sep=None, thousands=',')
stock_data_df['date'] = pd.to_datetime(stock_data_df['date'], format="%Y/%m/%d")
stock_data_df = stock_data_df.set_index('date')
calculate_impact(stock_data_df, 4)
stock_data_pct_change_df = (stock_data_df.pct_change() * 100).round(2)

#
# combining trend data and stock data
#

# result_df = pd.concat([combined_trend_data_df, stock_data_df, stock_data_pct_change_df], axis=1, sort=False)
result_df = pd.merge(combined_trend_data_df, stock_data_df, on=['date'], how='right')
print(result_df)
result_df.fillna(0, inplace=True)
print(result_df)
result_df.reset_index(inplace=True)
result_df.set_index('date', drop=False, inplace=True)
result_df.sort_index(inplace=True)
result_df = remove_weekends(result_df)
stock_trend_combined = result_df.to_csv(
    "/home/randilu/fyp_integration/Impact-Analysis-Module/data/interim/trend_data/stock_trend_combined.csv",
    sep='\t', encoding='utf-8', index=False)

formated_df = pd.read_csv(
    "/home/randilu/fyp_integration/Impact-Analysis-Module/data/interim/trend_data/stock_trend_combined.csv",
    sep='\t', encoding='utf-8')
formated_df.columns = formated_df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(',
                                                                                                    '').str.replace(')',
                                                                                                                    '').str.replace(
    '\'', '').str.replace(',', '').str.replace('.', '_')
formated_df = formated_df.dropna()
formated_df['kw_max'] = formated_df['kw_max'].str.replace('(', '').str.replace(')', '').str.replace('\'',
                                                                                                    '').str.replace(',',
                                                                                                                    '').str.replace(
    '.', '_')
print(formated_df.head())
# formated_df = rename_duplicate_max_values(formated_df)
add_impact_from_changepoints(
    '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/changepoints/effective_points.csv',
    formated_df, 7)
# add_impact(formated_df)
print(formated_df.head())
formated_df.to_csv(
    "/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/trend_data/stock_trend_formated.csv",
    sep='\t', encoding='utf-8', index=False)
