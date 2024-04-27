from django.urls import path, include

from .views import *


urlpatterns = [
    path("all/", OddDataViewSet.as_view({"get": "list"})),
    path("today/", OddDataViewSet.as_view({"get": "retrieve"})),
]
