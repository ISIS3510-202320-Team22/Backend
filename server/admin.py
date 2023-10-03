from django.contrib import admin
from .models import Post, User, Category

# Register your models here.
admin.site.register([Post, User, Category])
