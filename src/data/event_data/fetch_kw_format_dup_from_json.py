import json
import math

import pandas as pd
from pandas.io.json import json_normalize
from src.data.fetch_trend_data_utils import display_max_cols, save_dictionary_to_csv, read_json_data_from_file

# company_name = 'kelani_valley'
# display_max_cols(10)
# jfile = "/home/randilu/fyp_integration/Impact-Analysis-Module/data/external/events/eem/KelaniValleyPlantations2.json"


def get_events_from_json(company_name, jfile):
    events = read_json_data_from_file(jfile)
    events_df = json_normalize(events)
    events_df['date'] = pd.to_datetime(events_df['date'], format="%d/%m/%Y")
    events_df['date'] = events_df['date'].dt.date
    print(events_df)
    events_df.columns = events_df.columns.map(lambda x: x.split(".")[-1])

    print(events_df)
    # for i, row in events_df.iterrows():
    #     list = events_df['keywords'][i]
    #     events_df['keywords'][i] = list[0]

    # events_df.drop(columns='keywords', inplace=True)
    events_df.rename(columns={'content': 'event'}, inplace=True)
    events_df.rename(columns={'keywords': 'keyword_1'}, inplace=True)
    events_df.dropna(inplace=True)
    events_df['event_no'] = events_df.index
    # events_df.drop_duplicates(subset='keyword_1', keep="last", inplace=True)
    # events_df.reset_index(drop=True, inplace=True)
    print(events_df)
    events = events_df[['event_no', 'event', 'keyword_1']]
    # events.drop_duplicates(subset='keyword_1', keep="last", inplace=True)
    # events.reset_index(drop=True, inplace=True)
    events.to_csv(
        '/home/randilu/fyp_integration/Impact-Analysis-Module/src/data/dictionaries/' + company_name + '_event_dictionary.csv',
        sep=',', encoding='utf-8', index=False)
    print(events)

    df_of_kw_sent = events_df[['event_no', 'date', 'keyword_1', 'sentiment']]
    print(df_of_kw_sent)
    df_of_kw_sent['sentiment'] = df_of_kw_sent['sentiment'].apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)
    print(df_of_kw_sent)
    df_of_kw_sent = df_of_kw_sent[df_of_kw_sent.sentiment != 0.0]
    df_of_kw_sent.reset_index(drop=True, inplace=True)
    kw_sent_list = []

    for row in df_of_kw_sent.iterrows():
        index, data = row
        kw_sent_list.append(data.tolist())
    print(kw_sent_list)
    return kw_sent_list

# #
# # run manually
# #
# get_events_from_json(company_name, jfile)