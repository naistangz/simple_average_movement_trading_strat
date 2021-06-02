import requests
from datetime import date, timedelta, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from alpha_vantage.timeseries import TimeSeries
import os


class NoApiKeyFoundError(Exception):
    pass


class TradeAnalysis:

    date_formatter = '%Y-%m-%d'
    currency_formatter = lambda x: f'£{x:.2f}'

    def __init__(self,
                 api_key='GMYKXRVYJG8POKZQ',
                 digital_currency='BTC',
                 market='GBP',
                 function='DIGITAL_CURRENCY_DAILY'):
        self.function = function
        self.api_key = api_key
        self.symbol = digital_currency
        self.market = market
        self.result = self.calculate_simple_moving_average()

    def get_api_key(self):
        # raise error if api key env variable doesn't exist
        try:
            api_key = os.environ.get('ALPHAVANTAGE_API_KEY', None)
        except KeyError:
            # raise no api key error found here
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

    def calculate_simple_moving_average(self, rows=None):
        """
        :rows: -> By default shows top 10 rows
        Returns a dataframe with closing_price, simple moving average over 3 and 7 days and trade signals
                   date  closing_price        SMA_3        SMA_7 signal
        0   2020-01-01  5085.52830400          NaN          NaN   None
        1   2020-01-02  4919.46303040          NaN          NaN   None
        ...
        10  2020-01-11  5664.05186240  5658.110030  5584.623067    BUY
        11  2020-01-12  5780.56027520  5744.558514  5667.982592    BUY
        12  2020-01-13  5727.84652160  5724.152886  5703.530678    BUY
        13  2020-01-14  6221.98146240  5910.129420  5770.596238    BUY
        14  2020-01-15  6230.03259840  6059.953527  5847.821564    BUY
        ....
        19  2020-01-20  6103.57326400  6181.956487  6207.316893   SELL
        20  2020-01-21  6169.73382720  6139.598566  6199.852945   SELL
        21  2020-01-22  6131.82992640  6135.045673  6185.823992   SELL
        """
        # iloc integer position based vs loc label-location based
        # : selection of all rows
        # ,1 index of first column
        df = self.construct_data_frame()
        df['SMA_3'] = df.iloc[:,1].rolling(window=3).mean()
        df['SMA_7'] = df.iloc[:,1].rolling(window=7).mean()
        df['signal'] = df.apply(self.conditions, axis=1)
        return df.head(rows)

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
            all_dates.append(day.strftime(self.date_formatter))
        return all_dates

    def plot_results(self, dataframe):
        df = dataframe
        plt.figure(figsize=(14, 7))
        plt.grid(True)
        # todo: set intervals e.g. monthly as all dates are crammed into x axis
        # todo: plot closing price...not sure why displaying incorrectly
        # plt.plot(df['date'], df['closing_price'], label='Closing price')
        plt.plot(df['date'], df['SMA_3'], label='SMA 3 days')
        plt.plot(df['SMA_7'], label='SMA 7 days')
        plt.title('Bitcoin price history 2020')
        plt.ylabel('Bitcoin GBP')
        # plt.format_ydata = self.currency_formatter
        plt.xlabel('Date')
        plt.xticks(rotation=90)
        plt.legend(loc='best')
        plt.savefig('results/results.png')
        plt.show()
        plt.close()
        return plt

    def conditions(self, dataframe):
        df = dataframe
        if df['SMA_3'] and df['SMA_7']:
            if (df['SMA_3'] > df['SMA_7']):
                return 'BUY'
            elif (df['SMA_3'] < df['SMA_7']):
                return 'SELL'
        else:
            return 0

if __name__ == '__main__':
    app = TradeAnalysis()
    # plot graph

    # Simple moving avg throughout the year
    print(app.plot_results(app.calculate_simple_moving_average(365)))

    # Simple moving avg first 30 days
    # print(app.plot_results(app.calculate_simple_moving_average(30)))

    # printing trading signals first 50, 20 days
    # print(app.calculate_simple_moving_average(20))
    # print(app.calculate_simple_moving_average(50))

    # printing trading signals throughout year
    print(app.calculate_simple_moving_average())

