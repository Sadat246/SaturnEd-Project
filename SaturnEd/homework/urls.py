from django.urls import path

from . import views

app_name = "homework"

urlpatterns = [
  path("", views.index, name="index"),
  path("cookies", views.cookies, name="cookies"),
  path("hw_list", views.hw_list, name="hw_list"),
  path("forms", views.forms, name="forms"),
  path("django_forms", views.django_forms, name="django_forms"),
  path("search_form", views.search_form, name="search_form"),
  path("list_view", views.list_view, name="list_view"),
  path("edit_hw", views.edit_hw, name="edit_hw"),
]
