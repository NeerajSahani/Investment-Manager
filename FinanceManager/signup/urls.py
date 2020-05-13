from django.urls import path
from django.contrib.auth import logout
from signup import views

app_name = 'signup'
urlpatterns = [
    path('signup/', views.Registration.as_view(), name='signupView'),
    path('login/', views.login_view, name='loginView'),
    path('logout/', views.logout_view, name='logoutView'),
    path('profile/<slug:slug>/', views.ProfileView.as_view(), name='profileView'),
    path('activate/<str:uidb64>/<slug:token>/', views.activate, name='activate'),
]
