from django.urls import path, include

from .views import *


urlpatterns = [
    path("all/", OddDataViewSet.as_view({"get": "list"})),
]
