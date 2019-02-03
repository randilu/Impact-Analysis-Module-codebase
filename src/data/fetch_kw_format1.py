import json
from pandas.io.json import json_normalize
from src.data.fetch_trend_data_utils import display_max_cols, save_dictionary_to_csv

display_max_cols(10)
jfile = "/home/randilu/fyp_impact analysis module/impact_analysis_module/data/external/events/KV_PLC.json"
with open(jfile, 'r') as f:
    jdata = json.load(f)

events = jdata['events']
events_df = json_normalize(events)
# print(events_df)
events_df.columns = events_df.columns.map(lambda x: x.split(".")[-1])
# print(events_df)
# events_df = events_df.groupby(events_df.columns, axis=1)

# new = events_df[['date', 'event']]
# # new.groupby(new.columns, axis=1).apply(lambda x: x.apply(lambda y: ','.join([l for l in y if l is not None]), axis=1))
# print(new)

s = events_df.melt('date')
s['Key'] = s.groupby(['variable', 'date']).cumcount()
df1 = s.pivot_table(index=['date', 'Key'], columns='variable', values=['value'], aggfunc='first')
df1.columns = df1.columns.droplevel()
df1 = df1.reset_index()
df1.columns = df1.columns.tolist()
# print(df1)
events = df1[['event', 'keyword_1']]
print(events)
events_dic = events.set_index('keyword_1').to_dict()
print(events_dic)

print(events_dic.get("event", "key not Found"))
# save the dictionary to csv
# save_dictionary_to_csv(events_dic,
#                        '/home/randilu/fyp_impact analysis module/impact_analysis_module/src/data/dictionaries/events_dic.csv')

df_of_kw_sent = df1[['keyword_1', 'sentiment']]
df_of_kw_sent.drop_duplicates(subset='keyword_1', keep="last", inplace=True)
df_of_kw_sent.reset_index(drop=True, inplace=True)
df_of_kw_sent['sentiment'] = df_of_kw_sent['sentiment'].apply(lambda x: round(x, 0))
df_of_kw_sent = df_of_kw_sent[df_of_kw_sent.sentiment != 0.0]
df_of_kw_sent.reset_index(drop=True, inplace=True)
print(df_of_kw_sent)
kw_sent_list = []

for row in df_of_kw_sent.iterrows():
    index, data = row
    kw_sent_list.append(data.tolist())
# kw = df_of_kw_sent.apply(lambda x: x.tolist(), axis=1)
# kw_plus_sentiment = kw.apply(lambda x: x.tolist(), axis=1)

print(kw_sent_list)

# new_df = df[['keyword', 'sentiment']]
# print(new_df)
