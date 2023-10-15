from django.urls import path

from . import views

urlpatterns = [
    path("", views.getLocation, name="getLocation"),
    path("forecast/<str:city_key>", views.forecast, name="oneday"),
    path("getLocation",views.getLocation, name="getLocation"),

]