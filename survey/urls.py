from django.urls import path
from . import views

app_name = 'survey'
urlpatterns = [
    # ex: /survey/
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.indexView, name='index'),
    path('register/', views.registerView, name='register'),
    path('login/', views.loginView, name='login'),
    path('home/', views.homeView, name='home'),
    path('logout/', views.logoutUser, name='logout'),
]
