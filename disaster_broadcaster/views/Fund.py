from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from disaster_broadcaster.paginate import paginate
from disaster_broadcaster.models.Fund import Fund
from disaster_broadcaster.serializers.Fund import (
  FundCreateSerializer,
  FundGeneralSerializer,
  FundUpdateSerializer
)

class FundViewset(viewsets.ViewSet):
  permission_classes=(AllowAny,)

  # GET
  def list(self, request):
    page = request.GET.get("page")
    funds = Fund.objects.all()
    organization_id = request.GET.get("organization")
    disaster_id = request.GET.get("disaster")
    if organization_id is not None:
      funds = funds.fitler(organization_id=organization_id)
    elif disaster_id is not None:
      funds = funds.fitler(disaster_id=disaster_id)

    funds = funds.order_by("-date_created")
    if page is not None:
      funds = paginate(funds, page)
    serializer = FundGeneralSerializer(funds, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # POST
  def create(self, request):
    serializer = FundCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  # GET with id
  def retrieve(self, request, pk=None):
    fund = get_object_or_404(Fund.objects.all(), pk=pk)
    serializer = FundGeneralSerializer(fund)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # PATCH
  def partial_update(self, request, pk=None):
    fund = get_object_or_404(Fund.objects.all(), pk=pk)
    serializer = FundUpdateSerializer(fund, request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  # DELETE
  def destroy(self, request, pk=None):
    fund = get_object_or_404(Fund.objects.all(), pk=pk)
    fund.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
