from django.urls import path, re_path
from . import views

urlpatterns = [
    path('upload/cpp_file', views.upload_cpp_file, name='upload_cpp_file'),
    path('hello_world', views.hello_world, name='hello_world'),
]
