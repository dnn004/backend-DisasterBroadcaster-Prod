import os
import hashlib
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from disaster_broadcaster.bucket_delete import s3_delete

from .models.User import User
from .models.Post import Post
from .models.Comment import Comment
from .models.Reaction import Reaction
from .models.News import News
from .models.Fund import Fund
from .models.Category import Category
from .models.Disaster import Disaster
from .models.Country import Country
from .models.Organization import Organization

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  readonly_fields=('last_login',)

  # Fields visible for display
  list_display = ('id', 'username', 'password', 'email', 'avatar', 'country_id', 'answer', 'date_created', 'date_updated', 'is_deleted')
  list_filter = ('username', 'email')
  search_fields = ['username', 'email']

  # Fields visible for input
  fieldsets = (
    (None, {'fields': ('username', 'password')}),
    (_('Personal info'), {'fields': ('avatar', 'email', 'country_id', 'answer', )}),
    (_('Permissions'), {'fields': ['is_deleted']}),
    (_('Important dates'), {'fields': ('last_login',)}),
  )

  ordering = ('id', 'username',)
  save_on_top = True

  def save_model(self, request, obj, form, change):
    data = request.POST.dict()

    # change is boolean, True if user update, False if user create
    if not change:
      obj.set_password(data.get('password'))
      obj.answer = hashlib.md5(str(os.environ.get('SALT') + data.get('answer')).encode('utf-8')).hexdigest()
      obj.save()
    else:
      # Delete old avatar from S3
      user = User.objects.get(pk=obj.pk)
      if os.environ.get('DJANGO_DEBUG') == 'False':
        s3_delete(user.avatar.url)

      obj.save()

class PostInLine(admin.TabularInline):
  model = Post

class ReactionInLine(admin.TabularInline):
  model = Reaction

class CountryInLine(admin.TabularInline):
  model = Country



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'user_id', 'country_id', 'content', 'media', 'date_created',)
  save_on_top = True

  def save_model(self, request, obj, form, change):
    data = request.POST.dict()

    # change is boolean, True if user update, False if user create
    if not change:
      obj.save()
    else:
      # Delete old media from S3
      post = Post.objects.get(pk=obj.pk)
      if os.environ.get('DJANGO_DEBUG') == 'False':
        s3_delete(post.media.url)

      obj.save()

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ('id', 'user_id', 'post_id', 'comment', 'date_created',)
  save_on_top = True

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
  list_display = ('id', 'user_id', 'post_id', 'reaction',)
  save_on_top = True

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
  list_display = ('id', 'country_id', 'disaster_id', 'url', 'date_created', 'date_added', 'headline', 'content', 'media',)
  save_on_top = True

  def save_model(self, request, obj, form, change):
    data = request.POST.dict()

    # change is boolean, True if user update, False if user create
    if not change:
      obj.save()
    else:
      # Delete old media from S3
      news = News.objects.get(pk=obj.pk)
      if os.environ.get('DJANGO_DEBUG') == 'False':
        s3_delete(news.media.url)

      obj.save()

@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
  list_display = ('id', 'disaster_id', 'organization_id', 'fund_page', 'date_created',)
  save_on_top = True

@admin.register(Category)
class Category(admin.ModelAdmin):
  list_display = ('id', 'name', 'guide_url', 'description',)
  save_on_top = True

@admin.register(Disaster)
class DisasterAdmin(admin.ModelAdmin):
  list_display = ('id', 'country_id', 'category_id', 'date_happened',)
  save_on_top = True

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'emergency_url', 'emergency_number',)
  save_on_top = True

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'address', 'url', 'email', 'logo',)
  save_on_top = True

  def save_model(self, request, obj, form, change):
    data = request.POST.dict()

    # change is boolean, True if user update, False if user create
    if not change:
      obj.save()
    else:
      # Delete old logo from S3
      org = Organization.objects.get(pk=obj.pk)
      if os.environ.get('DJANGO_DEBUG') == 'False':
        s3_delete(org.logo.url)

      obj.save()
