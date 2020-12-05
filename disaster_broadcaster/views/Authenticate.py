from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404
from rest_framework import status
from django.http import JsonResponse
from disaster_broadcaster.models.User import User 
from disaster_broadcaster.serializers.User import UserGeneralSerializer
import hashlib
import json
import os

@csrf_exempt 
def AuthenticateUser(request):
  data = json.loads(request.body)
  username = data['username']
  password = data['password']
  user = get_object_or_404(User.objects.all(), username=username)
  if user.check_password(password):
    login(request, user)
    serializer = UserGeneralSerializer(user)
    return JsonResponse(data=serializer.data,status=status.HTTP_200_OK)
  else:
    return JsonResponse(data={}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt 
def LogoutUser(request):
  logout(request)
  return JsonResponse(data={}, status=status.HTTP_200_OK)

# If user inputs the correct answer, send email with link to password reset page
@csrf_exempt 
def PasswordReset(request):
  data = json.loads(request.body)
  email = data['email']
  user = get_object_or_404(User, email=email)

  answer = data['answer']
  hashed_answer = hashlib.md5(str(os.environ.get('SALT') + answer).encode('utf-8')).hexdigest()

  if user.answer == hashed_answer:
    login(request, user)
    send_mail(
      subject = 'Password Reset',
      message = 'This email has been sent because a password reset request ' +
      'has been made by an account associated with this email address. ' +
      '\n\nPlease follow the link to reset your password: \n\n',
      from_email = 'disaster.broadcaster@gmail.com',
      recipient_list = [email, ],
      fail_silently=False
    )
    return JsonResponse(data={}, status=status.HTTP_200_OK)
  else:
    return JsonResponse(data={}, status=status.HTTP_401_UNAUTHORIZED)