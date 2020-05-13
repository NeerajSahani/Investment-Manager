from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('dashboard/', views.InvestmentDashboard.as_view(), name='dashboard'),
    path('dashboard/<int:pk>/', views.InvestmentDetail.as_view(), name='detail'),
    path('dashboard/new/add-plans', views.InvestmentAddView.as_view(), name='add-plans'),
]
