from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create/create", views.create, name="create"),
    path("wiki/<str:entry>", views.show, name="show"),
    path("save/<str:entry>", views.save, name="save"),
    path("wiki/create/save/", views.create_save, name="create_save"),  
    path("edit/<str:entry>", views.edit, name="edit"),
    path("save_edited/<str:entry>", views.save_edited, name="save_edited"),
    path("random", views.randomize, name="random"),
    path("search/", views.index, name="search"),
    path("delete/<str:title>", views.delete, name="delete"),  
]