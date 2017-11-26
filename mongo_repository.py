from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from setup_data import get_predictions

base_polo_url = 'https://poloniex.com/public?command='\
    'returnChartData&currencyPair={}&start={}&end={}&period={}'
start_date = datetime.strptime('2015-01-01', '%Y-%m-%d')
end_date = datetime.now()
period = 86400


class MongoCrypto(object):

    def __init__(self, mongo):

        self.mongo = mongo
        self.cryptos = []

    def save_new_crypto_to_mongo(self, ticker):

        cryptos = self.mongo.db.cryptos

        if cryptos.find({'name': ticker}).count() > 0:
            return

        data = self.get_crypto_data(ticker)
        describe = data.describe()
        data = data.dropna(how='all')

        days = describe['close'][0]
        mean_price = describe['close'][1]
        mean_volume = describe['volume'][1]

        prices = data['close']
        train, test = get_predictions(prices, ticker)

        train = [float(i) for i in train]
        test = [float(i) for i in test]

        cryptos.insert({'name': ticker, 'prices': train, 'predicted_prices': test,
                        'days_analyzes': days, 'average_price': mean_price, 'average_volume': mean_volume})

    def get_crypto_data(self, poloniex_pair):
        poloniex_pair = "BTC_{}".format(poloniex_pair)
        json_url = base_polo_url.format(
            poloniex_pair,
            start_date.timestamp(),
            end_date.timestamp(),
            period
        )
        data_df = self.get_json_data(json_url, poloniex_pair)
        data_df = data_df.set_index('date')
        return data_df

    def get_json_data(self, json_url, cache_path):
        print('Downloading {}'.format(json_url))
        df = pd.read_json(json_url)
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(json_url, cache_path))
        return df

    def get_stored_cryptos(self):
        all_cryptos = []

        cryptos = self.mongo.db.cryptos

        for c in cryptos.find():
            all_cryptos.append(c['name'])

        return all_cryptos
