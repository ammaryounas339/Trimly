from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>", views.redirect_url, name="redirect_url"),]
