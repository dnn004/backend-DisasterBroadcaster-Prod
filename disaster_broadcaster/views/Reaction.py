from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from disaster_broadcaster.models.Reaction import Reaction
from disaster_broadcaster.serializers.Reaction import (
  ReactionCreateSerializer,
  ReactionGeneralSerializer,
  ReactionUpdateSerializer
)

class ReactionViewset(viewsets.ViewSet):
  permission_classes=(AllowAny,)

  # GET
  def list(self, request):
    serializer = ReactionGeneralSerializer(Reaction.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # POST
  def create(self, request):
    serializer = ReactionCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  # GET with id
  def retrieve(self, request, pk=None):
    reaction = get_object_or_404(Reaction.objects.all(), pk=pk)
    serializer = ReactionGeneralSerializer(reaction)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # PATCH
  def partial_update(self, request, pk=None):
    reaction = get_object_or_404(Reaction.objects.all(), pk=pk)
    serializer = ReactionUpdateSerializer(reaction, request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  # DELETE
  def destroy(self, request, pk=None):
    reaction = get_object_or_404(Reaction.objects.all(), pk=pk)
    reaction.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
