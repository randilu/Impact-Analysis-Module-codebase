import json
from pandas.io.json import json_normalize
from src.data.fetch_trend_data_utils import display_max_cols

display_max_cols(10)
jfile = "/home/randilu/fyp_impact analysis module/impact_analysis_module/data/external/events/eem_sample.json"
with open(jfile, 'r') as f:
    jdata = json.load(f)

events = jdata['events']
events_df = json_normalize(events)
print(events_df)
# df.columns = df.columns.map(lambda x: x.split(".")[-1])
# print(df.head())

df_of_kw_sent = events_df[['keyword', 'sentiment']]
print(df_of_kw_sent)
kw_sent_list=[]

for row in df_of_kw_sent.iterrows():
    index, data = row
    kw_sent_list.append(data.tolist())
# kw = df_of_kw_sent.apply(lambda x: x.tolist(), axis=1)
# kw_plus_sentiment = kw.apply(lambda x: x.tolist(), axis=1)

print(kw_sent_list)

# new_df = df[['keyword', 'sentiment']]
# print(new_df)