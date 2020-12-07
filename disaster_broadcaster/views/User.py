from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from disaster_broadcaster.paginate import paginate
from disaster_broadcaster.models.User import User
from disaster_broadcaster.serializers.User import (
  UserCreateSerializer,
  UserGeneralSerializer,
  UserUpdateSerializer,
  UserResetPasswordSerializer
)

class UserViewset(viewsets.ViewSet):
  permission_classes=(AllowAny,)

  def get_queryset(self):
    return User.objects.filter(is_deleted=False)

  # GET
  def list(self, request):
    page = request.GET.get('page')
    users = self.get_queryset()
    if page is not None:
      users = paginate(users, page)
    serializer = UserGeneralSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # POST
  def create(self, request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({
      'user': serializer.data,
      'token': Token.objects.create(user=user).key
    }, status=status.HTTP_201_CREATED)

  # GET with id
  def retrieve(self, request, pk=None):
    user = get_object_or_404(self.get_queryset(), pk=pk)
    serializer = UserGeneralSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # PATCH
  def partial_update(self, request, pk=None):
    user = get_object_or_404(self.get_queryset(), pk=pk)
    # If request is for updating user info that is not password

    # Check if loggedin user is the user requesting to update profile
    # Commented out for development easy testing, uncomment in production
    # if request.user != user.id:
    #   return Response(data={}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = UserUpdateSerializer(user, request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  # DELETE
  def destroy(self, request, pk=None):
    user = get_object_or_404(self.get_queryset(), pk=pk)
    # Check if loggedin user is the user requesting to update profile
    # Commented out for development easy testing, uncomment in production
    # if request.user != user.id:
    #   return Response(data={}, status=status.HTTP_401_UNAUTHORIZED)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  @action(detail=False, methods=['post'])
  def current_user(self, request):
    try:
      user = Token.objects.get(key=request.data.get('token')).user
      serializer = UserGeneralSerializer(user)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except:
      return Response({}, status=status.HTTP_404_NOT_FOUND)

  @action(detail=False, methods=['post'])
  def new_password(self, request):
    try:
      user = Token.objects.get(key=request.data.get('token')).user
      new_password = request.data.get('new_password')
      request.data['password'] = new_password
      serializer = UserResetPasswordSerializer(user, request.data)
      login(request, user)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
      serializer = UserGeneralSerializer(user)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except:
      return Response({}, status=status.HTTP_404_NOT_FOUND)
