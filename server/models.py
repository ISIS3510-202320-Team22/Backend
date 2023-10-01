from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

class Post(models.Model):
    post_id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category, related_name='posts')
    user = models.ForeignKey('User', related_name='posts', on_delete=models.CASCADE)


class User(models.Model):
    email = models.CharField(max_length=200)
