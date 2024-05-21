"""
URL configuration for bookStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import routers
from bookStoreAPI import views

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'author', views.AuthorViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'review', views.ReviewViewSet)

urlpatterns = [
    path('admin-nonsense-panel/', admin.site.urls), # should /admin/ is to obvious 
    path("", include("bookStoreApp.urls")),
    path("api/", include(router.urls)), # same reason as the admin
    path("api-auth-url/", include('rest_framework.urls', namespace='rest_framework')),  # same reason as the admin
]

urlpatterns += staticfiles_urlpatterns()