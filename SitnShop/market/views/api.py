from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Shop
from django.contrib.auth.models import User
from ..serializers import ShopSerializer, UserSerializer

# getshopList/
class ShopList(APIView):

    def get(self, request):
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)

    def post(self):
        pass


# getuserList/
class UserList(APIView):

    def get(self, request):
        users = User.objects.all().select_related('profile')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self):
        pass