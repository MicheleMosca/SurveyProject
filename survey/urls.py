from django.urls import path
from . import views

app_name = 'survey'
urlpatterns = [
    # ex: /survey/
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.indexView, name='index'),
    path('register/', views.registerView, name='register'),
]
