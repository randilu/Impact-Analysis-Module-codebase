import csv
import json
import codecs
import pandas as pd
import numpy as np
from pandas import DataFrame
from sklearn import preprocessing
import datetime

company_name = 'kelani_valley'


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


def add_impact_from_changepoints(file, stock_df, map_duration):
    print(stock_df)
    cp_df = pd.read_csv(file, index_col=False, sep='\t', encoding='utf-8')
    cp_df.drop(columns='impact', inplace=True)
    cp_df['isImpacted'] = 1
    # print(cp_df['date'])
    date_list = cp_df["date"].values
    modified_date_list = []
    for date in date_list:
        history = populate_date_range(date, map_duration)
        modified_date_list = list(set(modified_date_list + history))
        # modified_date_list = modified_date_list+history
    # modified_date_list.append(history)
    modified_cp_df = pd.DataFrame({'date': modified_date_list})
    modified_cp_df.sort_values(by=['date'], inplace=True)
    # print(modified_date_list)
    modified_cp_df = pd.merge(modified_cp_df, cp_df, on=['date'], how='left')
    modified_cp_df['isImpacted'].fillna(0, inplace=True)
    print(modified_cp_df)

    result = pd.merge(stock_df, modified_cp_df, on=['date'], how='left')
    print(result)
    result = result[['date', 'kw_max', 'max_value', 'daily_news_vector_sum', 'close', 'impact', 'isImpacted']]
    result['isImpacted'].fillna(0, inplace=True)
    result.to_csv(
        '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/events_impacted/' + company_name + '_final_combined_output.csv',
        sep='\t', encoding='utf-8', index=False)
    #
    # mapping the events with highest trend within a specified duration
    #
    mapped_df = map_events(result, map_duration)
    print(mapped_df)
    mapped_df.to_csv(
        '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/events_impacted/' + company_name + '_events_mapped.csv',
        sep='\t', encoding='utf-8', index=False)
    #
    # without modification to changepoint dates
    #
    impacted_df = pd.merge(cp_df, stock_df, on='date', how='inner')
    impacted_df.to_csv(
        '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/events_impacted/' + company_name + '_impacted.csv',
        sep='\t', encoding='utf-8', index=False)


def deserialize_json(file):
    data = pd.read_json(file)


def display_max_cols(cols):
    desired_width = 320
    pd.set_option('display.width', desired_width)
    np.set_printoptions(linewidth=desired_width)
    pd.set_option('display.max_columns', cols)


def split_sublist(sublist):
    return sublist[0], sublist[1], sublist[2], sublist[3]


def create_news_vector(df):
    col_list = list(df)
    del col_list[-1]
    return df[col_list].sum(axis=1)


def add_max_value(df):
    max_val = lambda x: max(x.min(), x.max(), key=abs)
    df['max_value'] = df.apply(max_val, axis=1)


def save_dictionary_to_csv(dic, file):
    with open(file, 'w') as f:
        w = csv.writer(f)
        w.writerow(dic.keys())
        w.writerow(dic.values())


def create_json_from_df(df):
    return json.dumps(json.loads(df.reset_index().to_json(orient='records')), indent=2)


def write_json_data_to_file(file, json_data):
    with open(file, 'w') as outfile:
        json.dump(json_data, outfile)
    # with open(file, 'wb') as f:
    #     json.dump(json_data, codecs.getwriter('utf-8')(f), ensure_ascii=False)


# calculate impact
def calculate_impact(stock_df, dp):
    series = stock_df['close']
    # Tail-rolling average transform
    rolling = series.rolling(window=4)
    rolling_mean = rolling.mean()
    stock_df['moving_avg'] = rolling_mean
    stock_df['impact'] = round(((series - rolling_mean) / rolling_mean) * 100, dp)
    stock_df.dropna(inplace=True)
    return stock_df


# rename duplicates
def rename_duplicate_keys(df, suffix='_'):
    appendents = (suffix + df.groupby(level=0).cumcount().astype(str).replace('0', '')).replace(suffix, '')
    return df.set_index(df.index + appendents)


def rename_duplicate_max_values(df):
    df.set_index('kw_max', inplace=True)
    new_df = rename_duplicate_keys(df)
    new_df.reset_index(level=0, inplace=True)
    new_df.rename(columns={'index': 'kw_max'}, inplace=True)
    return new_df


def create_date_range(date, days_before, days_after):
    date = pd.to_datetime(date)
    start_date = date + pd.DateOffset(days=-days_before)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = date + pd.DateOffset(days=days_after)
    end_date = end_date.strftime('%Y-%m-%d')
    return start_date, end_date


def populate_date_range(date, duration):
    date = pd.to_datetime(date)
    timestamps = pd.bdate_range(end=date, periods=duration).tolist()
    date_strings = [d.strftime('%Y-%m-%d') for d in timestamps]
    return date_strings


def map_events(df, duration):
    # iterate through each tupple in the dataframe
    new_df = pd.DataFrame(columns=['date', 'kw_max', 'max_value', 'daily_news_vector_sum', 'impact'])

    for line, row in enumerate(df.itertuples(), 1):
        if row.isImpacted == 1 and row.Index > duration:
            #
            # create a chunk of data frame from the whole data frame
            #
            temp_df = df.loc[row.Index - duration:row.Index]
            #
            # sorting the chunked data frame from max trend value
            #
            temp_df = temp_df.iloc[(-temp_df['max_value'].abs()).argsort()]
            if row.impact > 0:
                max_val = temp_df['max_value'].max()
            else:
                max_val = temp_df['max_value'].min()
            key = temp_df['kw_max'].iloc[0]
            daily_news_vec = temp_df['daily_news_vector_sum'].iloc[0]
            new_df = new_df.append(
                {'date': row.date, 'kw_max': key, 'max_value': max_val, 'daily_news_vector_sum': daily_news_vec,
                 'close': row.close, 'impact': row.impact}, ignore_index=True)
    return new_df
