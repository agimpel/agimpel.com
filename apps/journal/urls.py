from django.urls import path

from . import views

app_name = 'journal'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),    
    path('<slug>/', views.EntryView.as_view(), name='entry'),
]