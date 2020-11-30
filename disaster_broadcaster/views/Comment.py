from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from disaster_broadcaster.paginate import paginate
from disaster_broadcaster.models.Comment import Comment
from disaster_broadcaster.serializers.Comment import (
  CommentCreateSerializer,
  CommentGeneralSerializer,
  CommentUpdateSerializer
)

class CommentViewset(viewsets.ViewSet):
  permission_classes=(AllowAny,)

  # GET
  def list(self, request):
    page = request.GET.get('page')
    post = request.GET.get('post')
    comments = Comment.objects.all()

    # Filter for all comments under a post
    if post is not None:
      comments = comments.filter(post_id=post)

    # Oldest first
    comments = comments.order_by('date_created')
    if page is not None:
      comments = paginate(comments, page)
    serializer = CommentGeneralSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # POST
  def create(self, request):
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  # GET with id
  def retrieve(self, request, pk=None):
    comment = get_object_or_404(Comment.objects.all(), pk=pk)
    serializer = CommentGeneralSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)

  # PATCH
  def partial_update(self, request, pk=None):
    comment = get_object_or_404(Comment.objects.all(), pk=pk)
    # Check if loggedin user is the user requesting to update comment
    # Commented out for development easy testing, uncomment in production
    # if request.user != comment.user_id:
    #   return Response(data={}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = CommentUpdateSerializer(comment, request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  # DELETE
  def destroy(self, request, pk=None):
    comment = get_object_or_404(Comment.objects.all(), pk=pk)
    # Check if loggedin user is the user requesting to update comment
    # Commented out for development easy testing, uncomment in production
    # if request.user != comment.user_id:
    #   return Response(data={}, status=status.HTTP_401_UNAUTHORIZED)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
