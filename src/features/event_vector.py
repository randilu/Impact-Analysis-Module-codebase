import csv

import pandas as pd

from src.data.fetch_trend_data_utils import display_max_cols, create_json_from_df, write_json_data_to_file

display_max_cols(100)

impact_df = pd.read_csv(
    "/home/randilu/fyp_impact analysis module/impact_analysis_module/data/processed/events_impacted/impacted.csv"
    , sep='\t', encoding='utf-8')
print(impact_df)

event_df = impact_df[['date', 'kw_max', 'max_value', 'close_1', 'impact']]
event_df.set_index('kw_max', inplace=True)
print(event_df)

event_dictionary_df = pd.read_csv(
    '/home/randilu/fyp_impact analysis module/impact_analysis_module/src/data/dictionaries/event_dictionary.csv',
    sep=',', encoding='utf-8')
event_dictionary_df.set_index('keyword_1', inplace=True)
print(event_dictionary_df)
combined_event_impact_df = event_df.join(event_dictionary_df)
combined_event_impact_df.reset_index(level=0, inplace=True, )
combined_event_impact_df.rename(columns={'index': 'keyword'}, inplace=True)
combined_event_impact_df['date'] = pd.to_datetime(combined_event_impact_df.date)
combined_event_impact_df.sort_values(by=['date'], inplace=True)
combined_event_impact_df['date'] = combined_event_impact_df['date'].dt.strftime('%Y.%m.%d')
combined_event_impact_df.set_index('date', inplace=True)

print(combined_event_impact_df)
events_impact_json = create_json_from_df(combined_event_impact_df)

write_json_data_to_file(
    '/home/randilu/fyp_impact analysis module/impact_analysis_module/data/processed/final_output/impact_events.json',
    events_impact_json)
