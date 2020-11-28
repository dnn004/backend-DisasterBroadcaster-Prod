from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from disaster_broadcaster.paginate import paginate
from disaster_broadcaster.models.Disaster import Disaster
from disaster_broadcaster.serializers.Disaster import (
  DisasterCreateSerializer,
  DisasterGeneralSerializer,
  DisasterUpdateSerializer
)

class DisasterViewset(viewsets.ViewSet):
  permission_classes=(AllowAny,)

  # GET
  def list(self, request):
    page = request.GET.get('page')
    disasters = Disaster.objects.all()
    if page is not None:
      disasters = paginate(disasters, page)
    serializer = DisasterGeneralSerializer(disasters, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # POST
  def create(self, request):
    serializer = DisasterCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  # GET with id
  def retrieve(self, request, pk=None):
    disaster = get_object_or_404(Disaster.objects.all(), pk=pk)
    serializer = DisasterGeneralSerializer(disaster)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # PATCH
  def partial_update(self, request, pk=None):
    disaster = get_object_or_404(Disaster.objects.all(), pk=pk)
    serializer = DisasterUpdateSerializer(disaster, request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  # DELETE
  def destroy(self, request, pk=None):
    disaster = get_object_or_404(Disaster.objects.all(), pk=pk)
    disaster.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
