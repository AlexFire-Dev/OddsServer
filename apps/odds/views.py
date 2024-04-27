from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import serializers, viewsets, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from datetime import datetime

from .models import OddData
from .serializers import *


class OddDataViewSet(viewsets.ViewSet):
    """ ViewSet for Odds Data """

    def list(self, request) -> Response:
        queryset = OddData.objects.all().order_by("-od_add_time")
        serializer = OddDataSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request) -> Response:
        queryset = OddData.objects.filter(date=datetime.now().date()).order_by("-od_add_time")
        serializer = OddDataSerializer(queryset, many=True)
        return Response(serializer.data)
