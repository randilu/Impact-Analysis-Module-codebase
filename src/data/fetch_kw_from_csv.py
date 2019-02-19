import pandas as pd

from src.data.fetch_trend_data_utils import display_max_cols

display_max_cols(10)
company_name = 'kelani_valley'
events_csv_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/events/csv_files/' + company_name + '_events.csv'


def get_events_from_csv(company_name, events_csv_file):
    file = events_csv_file
    events = pd.read_csv(file, sep=',', encoding='utf-8')
    events.dropna(inplace=True)
    print(events)
    events['event_no'] = events.index
    keywords = events['keyword_1'].values
    keywords_list_format = []
    for item in keywords:
        item = [item]
        keywords_list_format.append(item)
    keywords_list_format
    events['keyword_1'] = pd.Series(keywords_list_format)

    print(events['keyword_1'])
    # for item in keywords
    # without date
    # events_df = events[['event', 'keyword_1', 'sentiment']]
    # with date

    events_df = events[['date', 'event', 'keyword_1', 'sentiment']]

    events.set_index('event_no', inplace=True)
    events.reset_index(level=0, inplace=True)
    events.rename(columns={'index': 'event_no'}, inplace=True)
    events = events[['event_no', 'event', 'keyword_1']]
    events.to_csv(
        '/home/randilu/fyp_integration/Impact-Analysis-Module/src/data/dictionaries/' + company_name + '_event_dictionary.csv',
        sep=',', encoding='utf-8', index=False)
    print(events)
    # events.set_index('keyword_1', inplace=True)
    # events = rename_duplicate_keys(events)
    # events.reset_index(level=0, inplace=True)
    # events.rename(columns={'index': 'keyword_1'}, inplace=True)
    # print(events)
    # events.set_index('date', inplace=True)
    # events = events[['event', 'keyword_1']]
    # events.to_csv(
    #     '/home/randilu/fyp_impact analysis module/impact_analysis_module/src/data/dictionaries/event_dictionary.csv',
    #     sep=',', encoding='utf-8', index=False)
    # print(events)

    events_df.reset_index(drop=True, inplace=True)
    events_df['event_no'] = events_df.index
    print(events_df)
    # without date
    # df_of_kw_sent = events_df[['keyword_1', 'sentiment']]
    # with date
    df_of_kw_sent = events_df[['event_no', 'date', 'keyword_1', 'sentiment']]
    print(df_of_kw_sent)
    df_of_kw_sent.reset_index(drop=True, inplace=True)
    kw_sent_list = []

    for row in df_of_kw_sent.iterrows():
        index, data = row
        kw_sent_list.append(data.tolist())

    print(kw_sent_list)
    return kw_sent_list

#
# #
# # run manually
# #
# get_events_from_csv(company_name, events_csv_file)
