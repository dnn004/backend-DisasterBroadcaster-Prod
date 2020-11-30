from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from disaster_broadcaster.paginate import paginate
from disaster_broadcaster.models.Country import Country
from disaster_broadcaster.serializers.Country import (
  CountryCreateSerializer,
  CountryGeneralSerializer,
  CountryUpdateSerializer
)

class CountryViewset(viewsets.ViewSet):
  permission_classes=(AllowAny,)

  # GET
  def list(self, request):
    page = request.GET.get('page')
    countries = Country.objects.all()
    if page is not None:
      countries = paginate(countries, page)
    serializer = CountryGeneralSerializer(countries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # POST
  def create(self, request):
    serializer = CountryCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  # GET with id
  def retrieve(self, request, pk=None):
    country = get_object_or_404(Country.objects.all(), pk=pk)
    serializer = CountryGeneralSerializer(country)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # PATCH
  def partial_update(self, request, pk=None):
    country = get_object_or_404(Country.objects.all(), pk=pk)
    serializer = CountryUpdateSerializer(country, request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  # DELETE
  def destroy(self, request, pk=None):
    country = get_object_or_404(Country.objects.all(), pk=pk)
    country.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
