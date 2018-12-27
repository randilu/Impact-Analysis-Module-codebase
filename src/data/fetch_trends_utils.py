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