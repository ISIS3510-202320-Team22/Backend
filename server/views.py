from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Post, User, Category
from .serializers import PostSerializer
import json

DEFAULT_CATEGORY = 'Generic'

# Create your views here.

# posts/
class PostList(APIView):
    parser_class = (FileUploadParser,)

    # def post(self, request, format=None):
    #     image = request.FILES['image']
    #     return Response(image.name, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Extract the list of category names from the request data (if provided)
        category_names = request.data.get('categories', [DEFAULT_CATEGORY])
        print(type(request.data.get('categories')))

        if not isinstance(category_names, list):
            return Response('Categories must be a list', status=status.HTTP_400_BAD_REQUEST)

        # Create or retrieve Category objects based on the category names
        categories = [Category.objects.get_or_create(name=category)[0] for category in category_names]

        # Remove the "categories" field from the request data since it's not a direct field of the Post model
        request.data.pop('categories', None)

        # Deserialize the remaining data from the request
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            # Save the Post object
            post = serializer.save()

            # Associate the Post with the specified categories
            post.categories.set(categories)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# posts/
# def get_post_detail(request, post_id):
#     if request.method == 'GET':
#         post = get_object_or_404(Post, post_id=post_id)
#         serialized_post = serializers.serialize('json', [post])
#         return JsonResponse(serialized_post, safe=False)


# @csrf_exempt
# def posts(request):
#     if request.method == 'GET':
#         posts = list(Post.objects.values())
#         return JsonResponse(posts, safe=False)

#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))
#         user_id = data.get('user_id', None)

#         if user_id is None:
#             return HttpResponse('User ID is required', status=400)

#         try:
#             user = get_object_or_404(User, pk=user_id)
#         except User.DoesNotExist:
#             return HttpResponse('User does not exist', status=404)

#         text = data.get('text', '')

#         if not text:
#             return HttpResponse('Text is required', status=400)

#         image = request.FILES.get('image', None)

#         categories = data.get('categories', [DEFAULT_CATEGORY])

#         # If categores is not a list, return an error
#         if not isinstance(categories, list):
#             return HttpResponse('Categories must be a list', status=400)

#         for category_name in categories:
#             category, _ = Category.objects.get_or_create(name=category_name)
#             try:
#                 category.full_clean()
#                 category.save()
#             except:
#                 return HttpResponse('Category name is too long', status=400)


#         post = Post(text=text, user=user)
#         try:
#             post.full_clean()
#             post.save()
#         except:
#             return HttpResponse('Text is too long', status=400)

#         post.categories.set(Category.objects.filter(name__in=categories))

#         return HttpResponse('Post created', status=201)




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

@csrf_exempt
def users(request):
    if request.method == 'GET':
        users = list(User.objects.values())
        return JsonResponse(users, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email', None)

        if email is None:
            return HttpResponse('Email is required', status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User(email=email)
            try:
                user.full_clean()
            except:
                return HttpResponse('Email is too long or doesn\'t match domain', status=400)
            user.save()
        else:
            return HttpResponse('User already exists', status=400)

        return HttpResponse('User created', status=201)
