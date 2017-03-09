from django.contrib import admin
from board.models import Category, Post
from board.models import UserProfile


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(UserProfile)
