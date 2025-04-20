"""
URL configuration for db_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from db_project.views import community_list, community_home, profile, edit_profile, create_community, create_post, post_detail
urlpatterns = [ 
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("communities/", community_list, name="community_list"),
    path("profile/", profile, name="profile"),
    path("profile/edit", edit_profile, name="edit_profile"),
    path("communities/create", create_community, name="create_community"),
    path("communities/<str:community_name>", community_home, name="community_home"),
    path("communities/<str:community_name>/create_post", create_post, name="create_post"),
    path("communities/<str:community_name>/<int:post_id>/", post_detail, name="post_detail"),
]
