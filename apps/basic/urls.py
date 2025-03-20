from django.urls import path

from . import views

app_name = 'basic'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('imprint/', views.imprint, name='imprint'),
]