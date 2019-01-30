import pandas as pd
import numpy as np
from pandas import DataFrame
from sklearn import preprocessing


def normalize_trends(frame, kw_list):
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(frame.get(kw_list))
    df = DataFrame(x_scaled)
    rounded = df.round(2)
    rounded.index = frame.index
    df = frame.drop(columns=['isPartial'])
    columns = pd.DataFrame(columns=df.columns)
    rounded.columns = [columns]
    rounded.index = rounded.index.normalize()
    return rounded


# Remove weekends from a dataframe
def remove_weekends(dataframe):
    # Reset index to use ix
    dataframe = dataframe.reset_index(drop=True)
    weekends = []
    # Find all of the weekends
    for i, date in enumerate(dataframe['date']):
        if (date.weekday() == 5) or (date.weekday() == 6):
            weekends.append(i)
    # Drop the weekends
    dataframe = dataframe.drop(weekends, axis=0)
    return dataframe


def add_impact(df):
    df['isImpacted'] = 'NI'
    # iterate through each tupple in the dataframe
    for line, row in enumerate(df.itertuples(), 1):
        if abs(row.plantations_1) > 1.5:
            # and abs(row.max_value) > 0.5:
            df.at[row.Index, 'isImpacted'] = "I"
            # df.set_value(row.Index, 'isImpacted', 'I')
    # for row in df.itertuples():
    #     if df.at[row, 'plantations.1'] > 3 and df.at[row, 'max_value'] > 0.5:
    #         df.at[row, 'isImpacted'] = 'I'
    return


def add_impact_from_changepoints(file, stock_df):
    cp_df = pd.read_csv(file, index_col=False, sep='\t', encoding='utf-8')
    print(cp_df)
    impacted_df = pd.merge(cp_df, stock_df, on='date', how='inner')
    impacted_df.to_csv(
        '/home/randilu/fyp_impact analysis module/impact_analysis_module/data/processed/events_impacted/impacted.csv',
        sep='\t', encoding='utf-8', index=False)


def deserialize_json(file):
    data = pd.read_json(file)


def display_max_cols(cols):
    desired_width = 320
    pd.set_option('display.width', desired_width)
    np.set_printoptions(linewidth=desired_width)
    pd.set_option('display.max_columns', cols)


def split_sublist(sublist):
    return sublist[0], sublist[1]


def create_news_vector(df):
    col_list = list(df)
    del col_list[-1]
    return df[col_list].sum(axis=1)


def add_max_value(df):
    max_val = lambda x: max(x.min(), x.max(), key=abs)
    df['max_value'] = df.apply(max_val, axis=1)
