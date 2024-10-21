from rest_framework import serializers
from .models import *
from .helpers import *


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionT
        fields = "__all__"


class GeneratedPhotoSerialize(serializers.ModelSerializer):
    class Meta:
        model = GeneratedPhotoT
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileT
        fields = "__all__"