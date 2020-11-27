from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from disaster_broadcaster.paginate import paginate
from disaster_broadcaster.models.Organization import Organization
from disaster_broadcaster.serializers.Organization import (
  OrganizationCreateSerializer,
  OrganizationGeneralSerializer,
  OrganizationUpdateSerializer
)

class OrganizationViewset(viewsets.ViewSet):
  permission_classes=(AllowAny,)

  # GET
  def list(self, request):
    page = request.GET.get("page")
    orgs = Organization.objects.all()
    if page is not None:
      orgs = paginate(orgs, page)
    serializer = OrganizationGeneralSerializer(orgs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # POST
  def create(self, request):
    serializer = OrganizationCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  # GET with id
  def retrieve(self, request, pk=None):
    organization = get_object_or_404(Organization.objects.all(), pk=pk)
    serializer = OrganizationGeneralSerializer(organization)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # PATCH
  def partial_update(self, request, pk=None):
    organization = get_object_or_404(Organization.objects.all(), pk=pk)
    serializer = OrganizationUpdateSerializer(organization, request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  # DELETE
  def destroy(self, request, pk=None):
    organization = get_object_or_404(Organization.objects.all(), pk=pk)
    organization.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
