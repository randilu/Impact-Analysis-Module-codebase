import pandas as pd
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
        if (date.weekday() ==5) or (date.weekday() == 6):
            weekends.append(i)
    # Drop the weekends
    dataframe = dataframe.drop(weekends, axis=0)
    return dataframe
