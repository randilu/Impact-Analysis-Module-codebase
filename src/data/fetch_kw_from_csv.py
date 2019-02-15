import json
import math
from pandas.io.json import json_normalize
import pandas as pd
from src.data.fetch_trend_data_utils import display_max_cols, save_dictionary_to_csv, rename_duplicate_keys

display_max_cols(10)
file = "/home/randilu/fyp_impact analysis module/impact_analysis_module/data/external/events/events_of_plantation_industry_v1 - kelani_valley_events.csv"
events = pd.read_csv(file, sep=',', encoding='utf-8')
events.dropna(inplace=True)
# without date
# events_df = events[['event', 'keyword_1', 'sentiment']]
# with date
events_df = events[['date', 'event', 'keyword_1', 'sentiment']]

events.set_index('keyword_1', inplace=True)
events = rename_duplicate_keys(events)
events.reset_index(level=0, inplace=True)
events.rename(columns={'index': 'keyword_1'}, inplace=True)
print(events)
events.set_index('date', inplace=True)
events = events[['event', 'keyword_1']]
events.to_csv(
    '/home/randilu/fyp_impact analysis module/impact_analysis_module/src/data/dictionaries/event_dictionary.csv',
    sep=',', encoding='utf-8', index=False)
print(events)

events_df.reset_index(drop=True, inplace=True)
print(events_df)
# without date
# df_of_kw_sent = events_df[['keyword_1', 'sentiment']]
# with date
df_of_kw_sent = events_df[['date', 'keyword_1', 'sentiment']]
print(df_of_kw_sent)
df_of_kw_sent.reset_index(drop=True, inplace=True)
kw_sent_list = []

for row in df_of_kw_sent.iterrows():
    index, data = row
    kw_sent_list.append(data.tolist())

print(kw_sent_list)
