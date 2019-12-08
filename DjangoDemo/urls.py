"""DjangoDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.shortcuts import HttpResponse, redirect, render
from app import views

# def login(request):
#     # return HttpResponse("login")
#     return render(request, 'login.html')
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('login/', login),
    path('classes/', views.classes),
    path('add_class/', views.add_class),
    path('del_class/', views.del_class),
    path('edit_class/', views.edit_class),
    path('students/', views.students),
    path('add_student/', views.add_student),
    path('edit_student/', views.edit_student),
    path('del_student/', views.del_student),
    path('modal_add_class/', views.modal_add_class),
    path('modal_add_student/', views.modal_add_student),
    path('teachers/', views.teachers),
]
