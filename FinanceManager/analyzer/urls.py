from django.urls import path

from analyzer.base import update
from . import views
from django.views import generic

app_name = 'analyzer'
urlpatterns = [
    path('', views.IndexView.as_view(), name='indexView'),
    path('view/<slug:slug>/', views.detail, name='detail'),
    path('search', views.search, name='search'),
    path('get-reply', views.get_message, name='get-reply'),
    path('correction', views.report, name='report'),
    path('<slug:username>/view/', generic.TemplateView.as_view(template_name='analyzer/working.html'),
         name='viewProfile'),
    path('suggestion/', views.suggestion_view, name='suggestionView'),
    path('history/', generic.TemplateView.as_view(template_name='analyzer/working.html'), name='history'),
]
