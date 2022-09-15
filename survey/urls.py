from django.urls import path
from . import views

app_name = 'survey'
urlpatterns = [
    path('', views.indexView, name='index'),
    path('register/', views.registerView, name='register'),
    path('login/', views.loginView, name='login'),
    path('home/', views.homeView, name='home'),
    path('logout/', views.logoutUser, name='logout'),
    path('survey/', views.surveyView, name='survey'),
    path('collection/', views.collectionView, name='collection'),
    path('panel/', views.adminView, name='admin'),
    path('results/', views.resultsView, name='results'),
    path('access/', views.access, name='access'),
    path('shib/', views.shib, name='shib'),
    # path('prova/', views.prova, name='prova'),
]
