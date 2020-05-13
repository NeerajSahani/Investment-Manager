import os
import pandas as pd
from . import models
import yfinance as yf
from datetime import timedelta, date
from sklearn.preprocessing import scale
from django.conf.urls.static import settings
from sklearn.linear_model import LinearRegression


class Predict:
    def __init__(self, ticker=None, days=30, start=date.today()):
        # get all tickers
        self.model = None
        self.data = None
        self.ticker = ticker
        self.days = days
        self.start = start
        self.df = None
        self.days_gap = models.Company.objects.get(symbol=ticker).days_gap

    def get_data(self):
        name = str(date.today()) + '.csv'
        path = settings.MEDIA_ROOT + '/yahoo/' + self.ticker + '/'

        try:
            data = pd.read_csv(path + name)
            data.Date = data['Date'].astype('datetime64[ns]')
            data.set_index('Date', inplace=True)

        except FileNotFoundError:
            data = yf.download(self.ticker, end=self.start)
            data.dropna(inplace=True)
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
            try:
                # delete previous data
                os.remove(path + os.listdir(path)[0])
            except IndexError:
                pass
            data.to_csv(path + name)
        self.df = data.copy()
        data = data[['Open']]  # Droping rest columns
        self.data = data[:-1]

    def get_model(self):
        self.get_data()

        days_gap = self.days_gap
        test_size = 200
        if len(self.data) < test_size + days_gap:
            test_size = int(len(self.data) * .10)

        train_data = scale(self.data.iloc[:, 0:1][:-test_size])

        inputs = train_data
        x_train, y_train = [], []
        for i in range(days_gap, len(inputs)):
            x_train.append(inputs[i - days_gap:i, 0])
            y_train.append(inputs[i, 0])

        model = LinearRegression()
        model.fit(x_train, y_train)
        self.model = model

    def predict(self):
        self.get_model()
        for i in range(self.days):
            df = self.data.drop(self.data.index)
            a = self.data.iloc[:, 0:1][-self.days_gap:].values
            a = a.reshape(1, -1)
            df.loc[self.data.iloc[-1].name + timedelta(days=1)] = self.model.predict(a)
            self.data = self.data.append(df)

    def get_result(self, days=None):
        if days:
            self.days = days

        self.predict()

        future = self.data[-self.days:].Open
        s = future.nsmallest(int(self.days * 60 / 100))
        temp = []
        for key, val in zip(s.index, s):
            tmp = future[key:] - val
            temp.append((key, tmp.idxmax(), max(tmp)))

        res = sorted(temp, key=lambda x: x[2])[-1]
        # invest = future[res[0]:res[1]]
        context = {'all': self.df, 'df': self.data, 'days': self.days, 'ticker': self.ticker,
                   'result': res}  # res[start, end, profit]
        return context


def update(days=60):
    for company in models.Company.objects.all():
        ticker = company.symbol
        model = Predict(ticker=ticker, days=days)
        context = model.get_result()
        obj, created = models.Master.objects.get_or_create(company=company)
        obj.company = company
        obj.start = context['result'][0]
        obj.end = context['result'][1]
        obj.profit = round(context['result'][2], 2)
        if company.currency == 'USD':
            obj.profit *= 70
        obj.save()
