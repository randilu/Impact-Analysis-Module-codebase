import pandas as pd

from src.data.fetch_trend_data_utils import display_max_cols

display_max_cols(100)

impact_df = pd.read_csv(
    "/home/randilu/fyp_impact analysis module/impact_analysis_module/data/processed/events_impacted/impacted.csv"
    , sep='\t', encoding='utf-8')
print(impact_df)

event_df = impact_df[['date', 'kw_max', 'max_value', 'plantations_1']]
# impact_df['kw_max']
print(event_df)

