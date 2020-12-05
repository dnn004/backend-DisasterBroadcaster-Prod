from rest_framework import serializers
from disaster_broadcaster.models.User import User
from disaster_broadcaster.bucket_delete import s3_delete
import hashlib
import os

class UserCreateSerializer(serializers.ModelSerializer):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].required = True

  class Meta:
    model = User
    fields = ['id', 'password',  'username', 'email',
    'date_created', 'avatar', 'country_id', 'answer']

  def create(self, data):
    answer = data['answer']
    data['answer'] = hashlib.md5(str(os.environ.get('SALT') + answer).encode('utf-8')).hexdigest()
    return User.objects.create_user(**data)

class UserGeneralSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ['password', 'groups', 'user_permissions', 'is_deleted', 'is_staff', 'is_superuser']

class UserUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ['password']

  def update(self, instance:User, data):
    # Verification needs to be either fixed here later, or done in frontend
    if data.get('username'): instance.username = data.get('username')
    if data.get('email'): instance.email = data.get('email')
    if data.get('country_id'): instance.country_id = data.get('country_id')
    if data.get('avatar'): instance.avatar = data.get('avatar')
    if data.get('answer'):
      instance.answer = hashlib.md5(str(os.environ.get('SALT') + data.get('answer')).encode('utf-8')).hexdigest()

    instance.save()

    return instance

class UserResetPasswordSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['password',]

  def update(self, instance:User, data):
    if data.get('password'): instance.set_password(data.get('password'))
    
    super(User, instance).save()
    return instance