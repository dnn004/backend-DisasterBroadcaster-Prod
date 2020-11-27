from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from disaster_broadcaster.paginate import paginate
from disaster_broadcaster.models.News import News
from disaster_broadcaster.serializers.News import (
  NewsCreateSerializer,
  NewsGeneralSerializer,
  NewsUpdateSerializer
)

class NewsViewset(viewsets.ViewSet):
  permission_classes=(AllowAny,)

  # GET
  def list(self, request):
    page = request.GET.get("page")
    country_id = request.GET.get("country")
    news = News.objects.all()
    if country_id is not None:
      news = news.fitler(country_id=country_id)

    news = news.order_by("-date_added")
    if page is not None:
      news = paginate(news, page)
    serializer = NewsGeneralSerializer(news, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # POST
  def create(self, request):
    serializer = NewsCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  # GET with id
  def retrieve(self, request, pk=None):
    news = get_object_or_404(News.objects.all(), pk=pk)
    serializer = NewsGeneralSerializer(news)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # PATCH
  def partial_update(self, request, pk=None):
    news = get_object_or_404(News.objects.all(), pk=pk)
    serializer = NewsUpdateSerializer(news, request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  # DELETE
  def destroy(self, request, pk=None):
    news = get_object_or_404(News.objects.all(), pk=pk)
    news.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
