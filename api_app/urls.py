from django.urls import path
from . import api

urlpatterns = [
    # hello_world
    path('hello_world/', api.hello_world, name='hello_world'),
    path('get_gdb_result/', api.get_gdb_result, name='get_gdb_result'),
]
