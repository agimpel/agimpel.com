from django.urls import path, re_path

from . import views

app_name = 'journal'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),    
    path('<slug>/', views.EntryView.as_view(), name='entry'),
    re_path(r'^filter/((?:(?:[a-z0-9\-]+)(?:\.(?:[a-z0-9\-]+))+?/)+?)$', views.FilterView.as_view(), name="filter"),
]
