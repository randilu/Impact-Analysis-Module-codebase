import pandas as pd


# calculate impact
def calculate_impact(stock_df, dp):
    series = stock_df['close']
    # Tail-rolling average transform
    rolling = series.rolling(window=4)
    rolling_mean = rolling.mean()
    stock_df['impact'] = round(((series - rolling_mean) / rolling_mean) * 100, dp)
    stock_df.dropna(inplace=True)
    # stock_df.drop('close', axis=1, inplace=True)
    return stock_df


def calculate_impact_modeled(stock_df, dp):
    series = stock_df['y']
    modeled = stock_df['yhat']
    stock_df['impact'] = round(((series - modeled) / modeled) * 100, dp)
    stock_df.dropna(inplace=True)
    return stock_df


def get_impact_points(stock_df):
    impacts = stock_df[['impact']]
    impacts['abs_impact'] = abs(impacts['impact'])
    impacts = impacts.sort_values(by='abs_impact', ascending=False)
    # print(impacts)

    # Limit to 50 largest changepoints
    impacts = impacts[:50]
    impacts.sort_index(inplace=True, ascending=False)
    print(impacts)

    # Converting the index as date
    impacts.index = pd.to_datetime(impacts.index)
    print(impacts.index.dtype)
    impacts.reset_index(level=0, inplace=True)
    print(impacts)

    cp_df = impacts[['date', 'impact']]
    return cp_df

