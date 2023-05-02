from django.urls import path 
from . import views 
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("", views.fp, name="front page"),
    path("home/",views.course_list,name="home page"),
    path("apply/<int:id>",views.apply, name="apply"),
    path("instructor_summary/",views.InstructorSummaryView, name="instructor_summary"),
    path("instructor_summary/application/<int:pk>", views.ApplicationDetail.as_view(), name="application detail"),
    path("instructor_summary/offer/<int:pk>",views.sendOffer, name="send offer"),
    path("instructor_summary/reject/<int:pk>",views.rejectApp, name="reject application"),
    path("instructor_summary/application/resume/<int:pk>", views.show_pdf, name="application detail"),
    path("instructor_summary/offer/<int:pk>", views.sendOffer, name="send offer"),
    path("instructor_summary/reject/<int:pk>", views.rejectApp, name="send offer"),
    path("apply/error/",login_required(views.app_error.as_view()),name="apply error"),
    path("error/",views.semester_error, name='Semester error'),
    path("applications/", views.student_apps, name='Student applications'),
    path("applications/accept/<int:id>/", views.accept_offer, name="accept_offer"),
    path("applications/reject/<int:id>/", views.reject_offer, name="reject_offer"),
    path("notifications/", views.notification_list, name='notifications')
]