import requests
from datetime import date, timedelta, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import os


class NoApiKeyFoundError(Exception):
    pass


class TradeAnalysis:

    def __init__(self,
                 api_key='GMYKXRVYJG8POKZQ',
                 digital_currency='BTC',
                 market='GBP',
                 function='DIGITAL_CURRENCY_DAILY'):
        self.function = function
        self.api_key = api_key
        self.symbol = digital_currency
        self.market = market
        self.result = self.generate_trade_signals()

    def get_api_key(self):
        # raise error if api key env variable doesn't exist
        try:
            api_key = os.environ.get('ALPHAVANTAGE_API_KEY', None)
        except KeyError:
            api_key = self.api_key
        return api_key

    def make_api_call(self):
        base_url = 'https://www.alphavantage.co/query?'
        url = f'{base_url}function={self.function}&symbol={self.symbol}&market={self.market}&apikey={self.api_key}'
        response = requests.get(url)
        return response

    def parse_api_response(self):
        """:key
        prices = self.make_api_call()['Time Series (Digital Currency Daily)']['2020-06-01']['4a. close (GBP)']
        returns dictionary containing date and closing prices as key, value pairs
        e.g.

        '2020-01-07': '5453.40852000',
        '2020-01-02': '5124.1231123',
        '2020-01-01': '5061.76549900'
        }
        """
        prices = {}
        # year = 2020
        api_call = self.make_api_call()
        if api_call.status_code == 200:
            results = api_call.json()
            all_dates = self.get_all_dates()
            for date in all_dates:
                prices[date] = results['Time Series (Digital Currency Daily)'][date]['4a. close (GBP)']
        return prices

    def construct_data_frame(self):
        """:key
        constructs a table from a dictionary
        e.g
                   date   closing_price
        0    2020-01-01   5061.76549900
        1    2020-01-02   4896.47618740
        2    2020-01-03   5163.06618240
        3    2020-01-04   5169.49808340
        4    2020-01-05   5172.75972500
        """
        df = pd.DataFrame(self.parse_api_response().items(), columns=['date', 'closing_price'])
        return df

    def calculate_simple_moving_average(self):
        """:key
                 date  closing_price        SMA_3        SMA_7
        0  2020-01-01  5061.76549900          NaN          NaN
        1  2020-01-02  4896.47618740          NaN          NaN
        2  2020-01-03  5163.06618240  5040.435956          NaN
        3  2020-01-04  5169.49808340  5076.346818          NaN
        4  2020-01-05  5172.75972500  5168.441330          NaN
        5  2020-01-06  5453.40852000  5265.222109          NaN
        6  2020-01-07  5725.64312320  5450.603789  5234.659617
        7  2020-01-08  5662.87058120  5613.974075  5320.531772
        8  2020-01-09  5495.41621440  5627.976640  5406.094633
        9  2020-01-10  5762.01323880  5640.100011  5491.658498
        """
        df = self.construct_data_frame()
        df['SMA_3'] = df.iloc[:,1].rolling(window=3).mean()
        df['SMA_7'] = df.iloc[:,1].rolling(window=7).mean()
        self.plot_results(df)

    def get_all_dates(self):
        """:key
        Returns all dates as a list in 2020
        """
        # todo: dynamically get all dates given a year
        all_dates = []
        sdate = date(2020, 1, 1)
        edate = date(2021, 1, 1)
        delta = edate - sdate
        for i in range(delta.days):
            day = sdate + timedelta(days=i)
            all_dates.append(day.strftime('%Y-%m-%d'))
        return all_dates

    def plot_results(self, dataframe):
        df = dataframe
        plt.figure(figsize=(15, 10))
        plt.grid(True)
        plt.plot(df['date'], label='Date')
        plt.plot(df['SMA_3'], label='SMA 3 days')
        plt.plot(df['SMA_7'], label='SMA 7 days')
        plt.legend(loc=2)

    def generate_trade_signals(self):
        pass

if __name__ == '__main__':
    app = TradeAnalysis()
    # print(app.get_api_key())
    # print(app.make_api_call())
    # print(app.get_all_dates())
    # print(app.parse_api_response())
    print(app.calculate_simple_moving_average())
    # print(app.plot_results())

