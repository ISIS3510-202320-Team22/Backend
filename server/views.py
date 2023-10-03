from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Post, User, Category
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json

DEFAULT_CATEGORY = 'Generic'

# Create your views here.

# posts/
def get_post_detail(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, post_id=post_id)
        serialized_post = serializers.serialize('json', [post])
        return JsonResponse(serialized_post, safe=False)


@csrf_exempt
def posts(request):
    if request.method == 'GET':
        posts = list(Post.objects.values())
        return JsonResponse(posts, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id', None)

        if user_id is None:
            return HttpResponse('User ID is required', status=400)

        try:
            user = get_object_or_404(User, pk=user_id)
        except User.DoesNotExist:
            return HttpResponse('User does not exist', status=404)

        text = data.get('text', '')

        if not text:
            return HttpResponse('Text is required', status=400)

        image = request.FILES.get('image', None)

        categories = data.get('categories', [DEFAULT_CATEGORY])
        print(categories)

        # If categores is not a list, return an error
        if not isinstance(categories, list):
            return HttpResponse('Categories must be a list', status=400)

        for category_name in categories:
            category, _ = Category.objects.get_or_create(name=category_name)
            print(category)
            category.save()


        post = Post(text=text, user=user)
        post.save()

        post.categories.set(Category.objects.filter(name__in=categories))

        return HttpResponse('Post created', status=201)




# cateogires/
def get_posts_by_category(request, category_name):
    if request.method == 'GET':
        category = get_object_or_404(Category, name=category_name)
        posts = list(category.posts.values())
        return JsonResponse(posts, safe=False)


def get_categories(request):
    if request.method == 'GET':
        categories = list(Category.objects.values())
        return JsonResponse(categories, safe=False)





# users/
def get_posts_by_user(request, user_id):
    if request.method == 'GET':
        user = get_object_or_404(User, pk=user_id)
        posts = list(user.posts.values())
        return JsonResponse(posts, safe=False)
