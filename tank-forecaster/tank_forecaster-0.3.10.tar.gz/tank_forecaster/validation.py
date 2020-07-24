# libraries
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from tank_forecaster.decomp import generic_daily_decomp

def format_tank(dict_input, freq: str = '30min'):
    if dict_input == []:
        return None
    else:
        dict_input = sorted(dict_input, key=lambda x: x['read_time'])
        df = pd.DataFrame(dict_input)
        df.read_time = pd.to_datetime(df.read_time)
        df['y'] = df.volume.diff() * -1
        df = df[['read_time', 'y']].rename(columns={'read_time': 'ds'})
        df.y = df.y.clip(lower=0, upper=df.y.quantile(0.9999))
        df = df.set_index('ds').groupby(pd.Grouper(freq=freq)).sum()
        df.reset_index(level=0, inplace=True)
        return df.iloc[1:-1]


def format_sales(dict_input):
    if dict_input == []:
        return None
    else:
        dict_input = sorted(dict_input, key=lambda x: x['date'])
        dat = pd.DataFrame(dict_input)
        # only same tank df
        df = dat[dat['tank_type'] == dat.tank_type.iloc[-1]]
        df = df[['date', 'sales']]
        df.sales = df.sales.clip(lower=df.sales.quantile(0.015), upper=df.sales.quantile(0.995))
        df.rename(columns={'date': 'ds', 'sales': 'y'}, inplace=True)
        df['ds'] = pd.to_datetime(df['ds'], format='%Y-%m-%d')
    return df


def gen_past(df, freq='30min', periods=432):
    if len(df) == 0:
        now = datetime.now()
        end_0 = now - (now - datetime.min) % timedelta(minutes=30)
    else:
        end_0 = df.iloc[-1, 0]
    past = pd.date_range(end=end_0, freq=freq, periods=periods)
    past = pd.DataFrame(past)
    past.rename(columns={0: 'ds'}, inplace=True)
    past['ds'] = pd.to_datetime(past['ds'], format='%Y-%m-%d')
    return past


def validate_tank(tank_data, sales_data):

    # if no tank history
    if type(tank_data) != pd.core.frame.DataFrame:  # no historical sales data
        return 'no data'

    # add day of year for tank data / sales data
    sales_data['doy'] = sales_data['ds'].dt.dayofyear
    sales_data = sales_data.iloc[-100:]

    # create validation dataframe
    val_matrix = np.zeros((432, 2))
    val_df = pd.DataFrame(val_matrix,
                          columns=['ds',
                                   'doy'])


    # dynamically generate timestamps
    val_df['ds'] = gen_past(tank_data, freq='30min', periods=432)
    val_df['doy'] = val_df.ds.dt.dayofyear
    val_df['ts'] = val_df.ds.dt.time

    val_df = pd.merge(left=val_df, right=generic_daily_decomp, how='left', left_on='ts', right_on='ts')
    val_df = pd.merge(left=val_df, right=tank_data, how='left', left_on='ds', right_on='ds')
    val_df = pd.merge(left=val_df, right=sales_data, how='left', left_on='doy', right_on='doy')

    val_df.rename(columns={'ds_x': 'ds', 'y_x': 'actual', 'y_y': 'daily'}, inplace=True)
    val_df = val_df.loc[:, ['ds', 'ts', 'actual', 'daily', 'daily_multi']]

    # calculate generalized daily tank sticking curve from sales data
    val_df['base_est'] = (val_df.loc[:, 'daily'] * (1 / 48))
    est = val_df['base_est'] * val_df['daily_multi']
    val_df['estimated'] = est

    val_df = val_df.loc[:, ['ds', 'actual', 'estimated']]


    # data abnormalities adjustment
    diff = val_df.estimated - val_df.actual
    threshold = diff.abs().quantile(0.95)

    mask_adj = diff.abs() > threshold
    mask_tank = [not i for i in mask_adj]

    # val_df.loc[mask_adj, 'output'] = val_df.loc[mask_adj, 'adj_sales']
    # val_df.loc[mask_tank, 'output'] = val_df.loc[mask_tank, 'tank_vals']

    # missing data imputation
    mask_nan = val_df.actual.isna()
    mask_not_nan = [not i for i in mask_nan]

    val_df.loc[mask_nan, 'y'] = val_df.loc[mask_nan, 'estimated']
    val_df.loc[mask_not_nan, 'y'] = val_df.loc[mask_not_nan, 'actual']

    # for testing purposes, uncomment this
    # return val_df

    # for use in forecasting, uncomment this
    val_df.rename(columns={'ds_x': 'ds'}, inplace=True)
    return val_df[['ds', 'y']]
