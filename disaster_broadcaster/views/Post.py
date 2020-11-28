from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from disaster_broadcaster.paginate import paginate
from disaster_broadcaster.models.Post import Post
from disaster_broadcaster.serializers.Post import (
  PostCreateSerializer,
  PostGeneralSerializer,
  PostUpdateSerializer
)

class PostViewset(viewsets.ViewSet):
  permission_classes=(AllowAny,)

  # GET
  def list(self, request):
    page = request.GET.get('page')
    country_id = request.GET.get('country')
    personal = request.GET.get('personal')
    posts = Post.objects.all()
    if country_id is not None:
      posts = posts.filter(country_id=country_id)
    elif personal is not None:
      posts = posts.filter(user_id=request.user.id)

    posts = posts.order_by('-date_created')
    if page is not None:
      posts = paginate(posts, page)
    serializer = PostGeneralSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # POST
  def create(self, request):
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  # GET with id
  def retrieve(self, request, pk=None):
    post = get_object_or_404(Post.objects.all(), pk=pk)
    serializer = PostGeneralSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # PATCH
  def partial_update(self, request, pk=None):
    post = get_object_or_404(Post.objects.all(), pk=pk)
    # Check if loggedin user is the user requesting to update post
    # Commented out for development easy testing, uncomment in production
    # if request.user != post.user_id:
    #   return Response(data={}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = PostUpdateSerializer(post, request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  # DELETE
  def destroy(self, request, pk=None):
    post = get_object_or_404(Post.objects.all(), pk=pk)
    # Check if loggedin user is the user requesting to update post
    # Commented out for development easy testing, uncomment in production
    # if request.user != post.user_id:
    #   return Response(data={}, status=status.HTTP_401_UNAUTHORIZED)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
