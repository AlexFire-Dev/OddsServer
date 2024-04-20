from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models


User = get_user_model()


class OddDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OddData
        fields = '__all__'
