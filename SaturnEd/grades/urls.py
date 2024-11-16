from django.urls import path

from . import views

app_name = "grades"

urlpatterns = [
   path("", views.index, name="index"),
   path("instructions/", views.instructions, name="instructions"),
   path("cookies/", views.cookies, name="cookies"),
   path("forms/", views.forms, name="forms"),
   path("new_forms/", views.new_forms, name="new_forms"),
   path("new_score_report/", views.new_score_report, name="new_score_report"),
   path("finder/",views.finder,name="finder"),
   path("edit/", views.edit, name="edit"),
#    path("", views.movie_info, name="movie_info")
]