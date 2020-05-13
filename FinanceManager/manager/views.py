import datetime
from datetime import timedelta
from FinanceManager import plotting
from django.shortcuts import render
from django.utils.text import slugify
from django.views import generic
from . import models, forms
import pandas as pd, yfinance as yf
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class InvestmentDashboard(LoginRequiredMixin, generic.ListView):
    template_name = 'manager/dashboard.html'
    context_object_name = 'investment'

    def get_queryset(self):
        return models.Investment.objects.filter(user=self.request.user)


class InvestmentAddView(generic.CreateView):
    form_class = forms.InvestmentForm
    success_url = '/manager/dashboard'
    template_name = 'analyzer/form.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super(InvestmentAddView, self).get_context_data()
        context['title'] = 'Add Investment Plans'
        return context

    def dispatch(self, request, *args, **kwargs):
        self.user = slugify(request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print('User ', self.user)
        user = models.CustomUser.objects.get(slug=self.user)
        form.instance.user = user
        return super(InvestmentAddView, self).form_valid(form)


class InvestmentDetail(generic.DetailView):
    model = models.Investment
    template_name = 'manager/detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvestmentDetail, self).get_context_data()
        object_ = kwargs['object']
        real = yf.download(object_.company.symbol, start=object_.start_date)
        real.dropna(inplace=True)
        predicted = pd.read_csv(object_.file)
        predicted.set_index('date', inplace=True)
        try:
            predicted_today = predicted.loc[datetime.date.today()].open.values[-1]
        except:
            predicted_today = predicted.open.values[-1]

        df = real
        config = {
            'displaylogo': False,
            'scrollZoom': True,
            'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'drawclosedpath', 'drawcircle', 'drawrect',
                                    'eraseshape']
        }
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']), )
        fig.update_layout(
            height=330,
            template='plotly_white',
            xaxis_rangeslider_visible=False,
            margin=dict(t=0, b=0, l=0, r=0),
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=False, config=config)
        context['candlestick'] = plot_div

        fig_2 = go.Figure()
        fig_2.add_trace(go.Scatter(
            x=real.index,
            y=real.Open,
            name='Real'
        ))
        fig_2.add_trace(go.Scatter(
            x=predicted.index,
            y=predicted.open,
            name='Predicted'

        ))

        fig_2.update_layout(
            template='plotly_white',
            # title='Results',
            # xaxis_title="Date",
            # yaxis_title="Price",
            autosize=True,
            height=330,
            margin=dict(t=0, b=0, l=0, r=0),
            legend=dict(
                x=0.009,
                y=0.981,
                traceorder="normal",
                font=dict(
                    family="sans-serif",
                    size=12,
                    color="black"
                ),
                bordercolor="grey",
                bgcolor="white",
                borderwidth=1
            )
        )

        context['comparison'] = plot(fig_2, output_type='div', include_plotlyjs=False, config=config)
        start_value = int(real.Open.values[0])
        end_value = int(predicted.open.values[-1])
        context['gauge_chart'] = plotting.get_gauge_chart(start=start_value, end=end_value)
        context['base_price'] = start_value
        today = int(real.loc[datetime.date.today() - datetime.timedelta(days=3):datetime.date.today()].Open.values[-1])
        context['today_price'] = today
        context['today_predicted'] = predicted_today
        context['deviation'] = today / predicted_today * 100
        return context
