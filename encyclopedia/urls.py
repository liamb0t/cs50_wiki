from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
	path("", views.index, name="index"),
	path("new", views.new, name="new"),
	path("random", views.random, name="random"),
	path("edit", views.new, name="edit"),
	path("search", views.search, name="search"),
	path("<str:title>", views.displayEntry, name="title"),
]

