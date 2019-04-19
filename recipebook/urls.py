"""recipebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from recipebook.models import Author, Recipe
from . import views

admin.site.register(Author)
admin.site.register(Recipe)

#comment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>/', views.recipe, name='recipe'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('author/add/', views.add_author, name='add_author'),
    path('recipe/add/', views.add_recipe, name='recipe/add/'),
    path('confirmation/', views.add_recipe, name='confirmation'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('error/', views.error_view, name='error'),
    path('update/',views.edit_recipe, name='update'),
    path('profile/', views.profile, name='profile'),
    path('favorite/<int:recipe_id>', views.favorite, name='favorite')
]
