import sys
import pytz
import datetime as dt
from datetime import date, timedelta

import pandas as pd
from energyquantified import EnergyQuantified
from app.core.config import settings


def convert_date_to_utc(time_zone, dt_str, t_format="%Y-%m-%d"):
    if(dt_str == ''):
        return None
    if isinstance(dt_str, dt.date):
        dt_str = dt_str.strftime(t_format)
    naive = dt.datetime.strptime(dt_str, t_format)
    local = pytz.timezone(time_zone)
    local_date = local.localize(naive, is_dst=True)
    return local_date.astimezone(pytz.utc).replace(tzinfo=None)


def convert_date_to_utc_with_hours(time_zone, dt_str, t_format="%Y-%m-%d %H:%M:%S"):
    print('entering convert_date_to_utc_with_hours')
    print(time_zone, dt_str)
    if(dt_str == ''):
        return None
    if isinstance(dt_str, dt.date):
        dt_str = dt_str.strftime(t_format)
    naive = dt.datetime.strptime(dt_str, t_format)
    local = pytz.timezone(time_zone)
    local_date = local.localize(naive, is_dst=True)
    return local_date.astimezone(pytz.utc).replace(tzinfo=None)


def convert_date_from_utc(time_zone, dt_obj, is_string=True, t_format="%Y-%m-%d %H:%M:%S", str_format="%Y-%m-%d"):
    # print(f'from convert_date_from_utc --- > {dt_obj}')
    if(dt_obj is None):
        return None
    if isinstance(dt_obj, str):
        dt_obj = dt.datetime.strptime(dt_obj, t_format)
    utc = pytz.timezone('UTC')
    new_zone = pytz.timezone(time_zone)
    dt_obj = utc.localize(dt_obj)
    dt_obj = dt_obj.astimezone(new_zone).replace(tzinfo=None)
    if is_string:
        dt_obj = dt_obj.strftime(str_format)
    return dt_obj


def create_schedule_dates_from_local(local_start_date, local_end_date, time_zone='Europe/Sofia',  date_format='%Y-%m-%d'):

    try:
        if isinstance(local_start_date, str):

            local_start_date = dt.datetime.strptime(
                local_start_date, date_format)
        elif isinstance(local_start_date, dt.date):
            local_start_date = dt.datetime.combine(
                local_start_date, dt.time.min)
        if isinstance(local_end_date, str):

            local_end_date = dt.datetime.strptime(local_end_date, date_format)
        elif isinstance(local_end_date, dt.date):
            local_end_date = dt.datetime.combine(local_end_date, dt.time.min)

        local_end_date = local_end_date.replace(hour=23)

        start_date_utc = convert_date_to_utc_with_hours(
            time_zone, local_start_date)
        end_date_utc = convert_date_to_utc_with_hours(
            time_zone, local_end_date)
        return (start_date_utc, end_date_utc)
    except Exception as e:
        print("🚀 ~ file: utils.py ~ line 59 ~ e", e)
    return (None, None)


class Montel_Reader(object):

    def __init__(self):
        self.eq = self._create_eq()

    def _create_eq(self):
        api_key = settings.EQ_API_KEY
        eq = EnergyQuantified(api_key=api_key)
        return eq

    def get_data_df(self, q, begin_dt, end_dt):
        curves = self.eq.metadata.curves(q=q)
        curve = curves[0]
        timeseries = self.eq.timeseries.load(
            curve,
            begin=begin_dt,
            end=end_dt
        )
        return timeseries.to_dataframe()


class Spot(object):

    MARKETS = ['BG Price Spot EUR/MWh IBEX H Actual', 'GR Price Spot EUR/MWh ENEX H Actual', 'RO Price Spot EUR/MWh OPCOM H Actual',
               'HU Price Spot EUR/MWh HUPX H Actual', 'DE Price Spot EUR/MWh EPEX H Actual']

    def __init__(self, montel_reader, start_date, end_date):
        self.montel_reader = montel_reader
        self.start_date = convert_date_to_utc('Europe/Sofia', start_date)
        self.end_date = convert_date_to_utc('Europe/Sofia', end_date)

    def get_data(self):

        cet_start_date = convert_date_from_utc(
            'Europe/Prague', self.start_date, False)
        cet_end_date = convert_date_from_utc(
            'Europe/Prague', self.end_date, False)
        # cet_date = convert_date_from_utc(
        #     'Europe/Prague', dt.datetime.utcnow() - timedelta(days=2), False)

        final_df = pd.DataFrame()
        cols = []
        for spot_name in self.MARKETS:
            df = self.montel_reader.get_data_df(
                q=spot_name, begin_dt=cet_start_date, end_dt=cet_end_date)

            if final_df.empty:
                final_df = df
            else:
                final_df = pd.concat([final_df, df], axis=1)
            cols.append(spot_name.split(' ')[0] + '_Pr')

        if not final_df.empty:
            final_df.index = final_df.index.tz_convert('UTC').tz_localize(None)
            final_df.columns = cols
            final_df = final_df.reset_index()
            final_df.rename(columns={'date': 'utc'}, inplace=True)
            final_df['H24'] = final_df['utc'].apply(
                lambda x:  convert_date_from_utc('CET', x, False).hour + 1)
            cols = ['utc', 'H24'] + cols
            final_df = final_df[cols]

        # print(final_df)
        return final_df


# reader = Montel_Reader()
# sql_client = Ged_sql_client_m()
# scraper = Dam_4m(reader, sql_client)
# data = scraper.get_data()
# scraper.update_db(data)
