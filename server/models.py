import json
from django.db import models
from django.forms import ValidationError
from django.core import serializers


def validate_email_domain(email):
    accepted_domains = {'uniandes.edu.co'}
    try:
        domain = email.split('@')[1]
    except IndexError:
        return ValidationError('Email must contain a single @ symbol')

    if domain not in accepted_domains:
        raise ValidationError(f'Email domain must be one of the accepted domains')


def object_to_json(object):
    return json.dumps(serializers.serialize('json', [object])[0]['fields'])


# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=200, unique=True, validators=[validate_email_domain])

    def __str__(self) -> str:
        return self.email

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    reported = models.BooleanField(default=False)
    text = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self) -> str:
        return str(self.id) + ' - ' + self.text

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    posts = models.ManyToManyField(Post, related_name='categories')
    reported = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
