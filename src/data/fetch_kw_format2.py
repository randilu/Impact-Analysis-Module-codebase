import json
import math
from pandas.io.json import json_normalize
from src.data.fetch_trend_data_utils import display_max_cols, save_dictionary_to_csv

display_max_cols(10)
jfile = "/home/randilu/fyp_impact analysis module/impact_analysis_module/data/external/events/Kelani_Valley_Plantaitions_PLC_v2.json"
with open(jfile, 'r') as f:
    jdata = json.load(f)

events = jdata['events']
events_df = json_normalize(events)
print(events_df)
events_df.columns = events_df.columns.map(lambda x: x.split(".")[-1])

for i, row in events_df.iterrows():
    list = events_df['keywords'][i]
    events_df['keywords'][i] = list[0]

# events_df.drop(columns='keywords', inplace=True)
events_df.rename(columns={'content': 'event'}, inplace=True)
events_df.rename(columns={'keywords': 'keyword_1'}, inplace=True)
events_df.drop_duplicates(subset='keyword_1', keep="last", inplace=True)
events_df.reset_index(drop=True, inplace=True)
print(events_df)

events = events_df[['event', 'keyword_1']]
# events.drop_duplicates(subset='keyword_1', keep="last", inplace=True)
# events.reset_index(drop=True, inplace=True)
events.to_csv(
    '/home/randilu/fyp_impact analysis module/impact_analysis_module/src/data/dictionaries/event_dictionary.csv',
    sep=',', encoding='utf-8', index=False)
print(events)

df_of_kw_sent = events_df[['keyword_1', 'sentiment']]
print(df_of_kw_sent)
df_of_kw_sent['sentiment'] = df_of_kw_sent['sentiment'].apply(lambda x: 1 if x > 0 else -1 if x == 0 else 0)
print(df_of_kw_sent)
df_of_kw_sent = df_of_kw_sent[df_of_kw_sent.sentiment != 0.0]
df_of_kw_sent.reset_index(drop=True, inplace=True)
kw_sent_list = []

for row in df_of_kw_sent.iterrows():
    index, data = row
    kw_sent_list.append(data.tolist())

print(kw_sent_list)
