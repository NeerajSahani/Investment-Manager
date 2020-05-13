from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.text import slugify
from plotly.offline import plot
import plotly.graph_objects as go
from . import chatbot_utilities
from analyzer import models, forms
from .base import Predict, Predict
from django.views import generic
from django.core import mail
import datetime
from FinanceManager import plotting


# Create your views here.


class IndexView(generic.ListView):
    model = models.Company
    template_name = 'analyzer/index.html'
    context_object_name = 'company'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['Best'] = models.Master.objects.all().order_by('-profit')[:10]
        context['Tags'] = models.Tag.objects.all()
        return context


def data_view(request, *args, **kwargs):
    days = 30
    if request.GET.get('days'):
        days = int(request.GET.get('days'))

    slug = kwargs.get('slug')
    data = models.Company.objects.get(slug=slug)
    data.views += 1
    model = Predict(ticker=data.symbol, days=days)
    context = model.get_plot()
    context['data'] = data
    data.save()
    return render(request, 'analyzer/detailView.html', context)


def search(request, *args, **kwargs):
    key = request.GET.get('s')
    queryset = models.Company.objects.filter(
        Q(name__contains=key) | Q(tag__tag__contains=key) | Q(symbol__exact=key)).distinct()
    return render(request, 'analyzer/search.html', {'data': queryset})


def suggestion_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = forms.SuggestionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            msg = obj.user + ' Submitted Feedback \n' + obj.suggestion
            mail.mail_admins('Report', message=msg)
            messages.success(request, "Thanks for Suggestion we'll contact you soon")
            return redirect('analyzer:indexView')
    else:
        form = forms.SuggestionForm()
        return render(request, 'analyzer/form.html', {'form': form, 'title': 'Suggestion'})


def get_message(request, *args, **kwargs):
    que = request.GET.get('question')
    ans = chatbot_utilities.get_answer(que)
    context = {
        'answer': ans
    }
    return JsonResponse(context)


def report(request, *args, **kwargs):
    que = request.GET.get('question')
    chatbot_utilities.correction(que)
    print(que, 'Got')
    context = {
        'answer': 'Thanks for support'
    }
    return JsonResponse(context)


def detail(request, *args, **kwargs):
    days = 30
    if request.GET.get('days'):
        days = int(request.GET.get('days'))

    slug = kwargs.get('slug')
    data = models.Company.objects.get(slug=slug)
    data.views += 1
    model = Predict(ticker=data.symbol, days=days)
    context = model.get_result()
    context['data'] = data
    data.save()
    df = context['df']
    invest = df[context['result'][0]:context['result'][1]]
    start_value = int(df.loc[context['result'][0] - datetime.timedelta(days=3):context['result'][0]].Open.values[-1])
    end_value = int(df.loc[context['result'][1] - datetime.timedelta(days=3):context['result'][1]].Open.values[-1])

    config = {
        'displaylogo': False,
        'scrollZoom': True,
        'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'drawclosedpath', 'drawcircle', 'drawrect',
                                'eraseshape']
    }
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.Open[:-context['days']].index,
        y=df.Open[:-context['days']],
        name='Real',
        line=dict(width=3),

    ))
    fig.add_trace(go.Scatter(
        x=df.Open[-context['days']:].index,
        y=df.Open[-context['days']:],
        name='Predicted',
        line=dict(width=4),
    ))
    fig.add_trace(go.Scatter(
        x=invest.index,
        y=invest.Open,
        line=dict(width=4),
        name='Best Investment Period'
    ))
    fig.update_layout(
        title='Results',
        xaxis_title="Date",
        yaxis_title="Price",
        autosize=True,
        margin=dict(t=25, b=0, l=5, r=0),
        legend_orientation="h",
        xaxis_range=[str(datetime.date.today() - datetime.timedelta(days=120)),
                     datetime.date.today() + datetime.timedelta(days=60)]
    )

    fig.update_layout(
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
    context['plot'] = plot(fig, output_type='div', include_plotlyjs=False, config=config)
    df = context['all']
    fig_candle = go.Figure()
    fig_candle.add_trace(
        go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
    fig_candle.update_layout(xaxis_rangeslider_visible=False)
    fig_candle.update_layout(
        height=330,
        template='plotly_white',
        xaxis_rangeslider_visible=False,
        margin=dict(t=0, b=0, l=0, r=0),
    )
    context['candle'] = plot(fig_candle, output_type='div', include_plotlyjs=False, config=config)
    del context['all']

    context['bullet'] = plotting.get_gauge_chart(start=start_value, end=end_value)

    return render(request, 'analyzer/detailView.html', context)
