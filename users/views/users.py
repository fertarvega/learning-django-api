#Django
from users import serializers
from django.shortcuts import render

#Django REST framework
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

#Permissions
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwnProfile

#Models
from django.contrib.auth.models import User
from users.models import Profile

#Serializer
from users.serializers.users import UserSerializer, NewUserSerializer, ProfileSerializer
from users.serializers.signup import UsersSignupSerializer
from users.serializers.verified import AccountVerificationSerializer

class UserListView (ListAPIView):
    ''' List all the user with pagination'''

    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination



# @api_view(['GET'])
# def users(request):
#     if request.method == 'GET':
#         users = User.objects.filter(is_staff=False)
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

class ProfileCompletionViewSet(mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    """ Complete a user information """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnProfile]



@api_view(['POST'])
def signup(request):

    if request.method == 'POST':
        serializer = UsersSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = NewUserSerializer(user).data
        return Response(data)

@api_view(['POST'])
def account_verification(request):
    """"""
    if request.method == 'POST':
        serializer = AccountVerificationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message':'Account verification sucess'}
        return Response(data, status=status.HTTP_200_OK)