from django.urls import path

from . import views

app_name = 'gallery'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),    
    path('<slug>/', views.CategoryView.as_view(), name='category'),
    path('trip/<slug>/', views.TripView.as_view(), name='trip'),
    path('image/<slug>', views.ImageView.as_view(), name='image')
]