from rest_framework import serializers
from .models import Shop
from django.contrib.auth.models import User

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        # fields = ('ShopName', 'ShopOwner', 'user')
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'