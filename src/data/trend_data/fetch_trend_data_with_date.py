import pandas as pd
from pytrends.request import TrendReq

# from src.data.fetch_kw_from_csv_no_duplicates import kw_sent_list
# from src.data.fetch_kw_from_csv import kw_sent_list
# from src.data.fetch_kw_format2 import kw_sent_list
# from data.external.kw_list import new_list
# from src.data.event_data.fetch_kw_format_dup_from_json import kw_sent_list
from src.data.fetch_trend_data_utils import normalize_trends, remove_weekends, add_impact, add_impact_from_changepoints, \
    split_sublist, create_news_vector, add_max_value, display_max_cols, calculate_impact, rename_duplicate_max_values, \
    create_date_range

# company_name = 'kelani_valley'
# stock_csv_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/stock-data-companies/' + company_name + '.csv'
# display_max_cols(30)


def fetch_trend_data_for_keywords(event_list, company_name, stock_csv_file):
    # pytrends = TrendReq(hl='en-US', tz=330)

    # kw_list = [[0, '2017-12-15', 'tea', '-1'], [1, '2017-01-15', 'floods', '-1']]
    kw_list = event_list
    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend1 = TrendReq()
    # list which contains set of data frames each corresponding to a keyword
    joined_trend_dfs_list = []
    for i, sub_list in enumerate(kw_list, start=0):
        event_no, date, kw_sub_list, sentiment = split_sublist(sub_list)
        int_sentiment = int(sentiment)
        start_date, end_date = create_date_range(date, 14, 7)
        interest_over_time_df1 = pd.DataFrame()
        print(kw_sub_list)
        for item in kw_sub_list:
            item = [item]
            print(item)
            # sub_list = [sub_list]
            # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
            pytrend1.build_payload(item, cat=0, timeframe=start_date + " " + end_date, geo='LK')

            # Interest Over Time
            interest_over_time_df1 = pytrend1.interest_over_time()
            if interest_over_time_df1.empty:
                continue
            rounded_df1 = normalize_trends(interest_over_time_df1, item)
            rounded_df1 *= int_sentiment
            rounded_df1 = rounded_df1.add_suffix('_' + str(event_no))
            frames = [rounded_df1]
            # joining the data frames and appending into above specified list
            joined_trend_dfs_list.append(pd.concat(frames))
            break
        # print(interest_over_time_df1)
        # print(interest_over_time_df2)
        # interest_over_time_df1 = pytrend1.interest_over_time()
        # if interest_over_time_df1.empty:
        #     continue

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
    file = stock_csv_file
    stock_data_df = pd.read_csv(file, sep=None, thousands=',')
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
    result_df.to_csv(
        '/home/randilu/fyp_integration/Impact-Analysis-Module/data/interim/trend_data/' + company_name + '_stock_trend_combined.csv',
        sep='\t', encoding='utf-8', index=False)

    formated_df = pd.read_csv(
        '/home/randilu/fyp_integration/Impact-Analysis-Module/data/interim/trend_data/' + company_name + '_stock_trend_combined.csv',
        sep='\t', encoding='utf-8')
    formated_df.columns = formated_df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(',
                                                                                                        '').str.replace(
        ')',
        '').str.replace(
        '\'', '').str.replace(',', '').str.replace('.', '_')
    formated_df = formated_df.dropna()
    formated_df['kw_max'] = formated_df['kw_max'].str.replace('(', '').str.replace(')', '').str.replace('\'',
                                                                                                        '').str.replace(
        ',',
        '').str.replace(
        '.', '_')
    print(formated_df.head())
    # formated_df = rename_duplicate_max_values(formated_df)
    add_impact_from_changepoints(company_name,
                                 '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/changepoints/' + company_name + '_effective_points.csv',
                                 formated_df, 7)
    # add_impact(formated_df)
    print(formated_df.head())
    formated_df.to_csv(
        '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/trend_data/' + company_name + '_stock_trend_formated.csv',
        sep='\t', encoding='utf-8', index=False)
