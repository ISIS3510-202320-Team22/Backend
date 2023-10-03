from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('posts/<int:id>', views.get_post_detail),
    path('posts/', views.posts),
    path('categories/<str:category_name>', views.get_posts_by_category),
    path('categories/', views.get_categories),
    path('users/<int:user_id>', views.get_posts_by_user),
]
