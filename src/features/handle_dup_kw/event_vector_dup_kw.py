import csv

import pandas as pd

from src.data.fetch_trend_data_utils import display_max_cols, create_json_from_df, write_json_data_to_file

display_max_cols(100)

impact_df = pd.read_csv(
    "/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/events_impacted/events_mapped.csv"
    , sep='\t', encoding='utf-8')
print(impact_df)

event_df = impact_df[['date', 'kw_max', 'max_value', 'close', 'impact']]
event_df['kw_max'], event_df['event_no'] = event_df['kw_max'].str.split('_', 1).str
event_df['event_no'].dropna(inplace=True)
event_df['event_no'] = event_df['event_no'].astype(int)

print(event_df)

event_dictionary_df = pd.read_csv(
    '/home/randilu/fyp_integration/Impact-Analysis-Module/src/data/dictionaries/event_dictionary.csv',
    sep=',', encoding='utf-8')

print(event_dictionary_df)
combined_event_impact_df = pd.merge(event_df, event_dictionary_df, on=['event_no'], how='left')
combined_event_impact_df.dropna(inplace=True)
columns = ['event_no', 'keyword_1']
combined_event_impact_df.drop(columns, inplace=True, axis=1)

print(combined_event_impact_df)
events_impact_json = create_json_from_df(combined_event_impact_df)
write_json_data_to_file(
    '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/final_output/impact_events.json',
    events_impact_json)
