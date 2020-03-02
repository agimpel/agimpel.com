from django.urls import path

from . import views

app_name = 'photostream'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),    
    path('<pk>', views.PhotoView.as_view(), name='photo'),
]