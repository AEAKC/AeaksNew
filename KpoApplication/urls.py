from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("task/", task),
    path("registration/", RegisterUser.as_view(), name='reg'),
    path("login/", LoginUser.as_view(), name='login'),
    path("courses/", course),
    path("courses_easy/", courseEasy),
    path("courses_medium/", courseMedium),
    path("courses_hard/", courseHard),
    path("logout/", logout_user),
    path("", main, name='main'),
    path("acc/", acc),
    path("completed_courses", courses_done),
    path("update_profile", update_profile),
    path("faq/",faq)
]
