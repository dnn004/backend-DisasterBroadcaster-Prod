from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from disaster_broadcaster.models.Category import Category
from disaster_broadcaster.serializers.Category import (
  CategoryCreateSerializer,
  CategoryGeneralSerializer,
  CategoryUpdateSerializer
)

class CategoryViewset(viewsets.ViewSet):
  permission_classes=(AllowAny,)

  # GET
  def list(self, request):
    serializer = CategoryGeneralSerializer(Category.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # POST
  def create(self, request):
    serializer = CategoryCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  # GET with id
  def retrieve(self, request, pk=None):
    category = get_object_or_404(Category.objects.all(), pk=pk)
    serializer = CategoryGeneralSerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # PATCH
  def partial_update(self, request, pk=None):
    category = get_object_or_404(Category.objects.all(), pk=pk)
    serializer = CategoryUpdateSerializer(category, request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  # DELETE
  def destroy(self, request, pk=None):
    category = get_object_or_404(Category.objects.all(), pk=pk)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
