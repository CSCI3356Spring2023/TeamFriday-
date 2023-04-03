from django.urls import path 
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", views.fp, name="front page"),
    path("home/",views.CourseListView.as_view(),name="home page"),
    path("apply/<int:id>",views.apply, name="apply"),
]