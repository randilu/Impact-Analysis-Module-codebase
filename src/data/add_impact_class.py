import pandas as pd

from src.data.fetch_trend_data_utils import add_impact

stock_trend_df = pd.read_csv(
    "/home/randilu/fyp_impact analysis module/impact_analysis_module/data/processed/trend_data/stock_trend_formated_plantations_from_2013_to_2017.csv",
    sep='\,', encoding='utf-8')
print(stock_trend_df)
stock_trend_df = stock_trend_df.drop(columns=['isImpacted'])
print(stock_trend_df)

add_impact(stock_trend_df)
print(stock_trend_df)
stock_trend_df.to_csv("/home/randilu/fyp_impact analysis module/impact_analysis_module/data/processed/trend_data/test.csv",
                   sep='\t', encoding='utf-8', index=False)
