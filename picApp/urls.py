from django.urls import path
from .views import search_child, submit_child

urlpatterns = [
    path('', submit_child, name="submit_child"),
    path('search/', search_child, name="search_child"),
]
