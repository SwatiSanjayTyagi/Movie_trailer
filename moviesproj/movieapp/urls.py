
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.data_search, name="data_search"),
    path('Trailer/',views.Trailer, name = "Trailer")
]
