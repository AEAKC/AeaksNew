from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User



class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("id","task_number", "title", "task_text", "course", "blocks")


class TestAdmin(admin.ModelAdmin):
    list_dispaly = ("test_input", "input_type", "for_task", " is_exception")


class CompletedTasksAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "exercise",
    )


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UsersInline(admin.StackedInline):
    model = Users
    can_delete = False
    verbose_name_plural = 'Profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsersInline,)

# Re-register UserAdmin


class CoursesAdmin(admin.ModelAdmin):
    list_display = ("number_of_course", "title", "text", "difficulty")


class BlockAdmin(admin.ModelAdmin):
    list_display = ("id", "number_of_block", "title", "course")


# class UsersAdmin(admin.ModelAdmin):
#     list_display = ("id", "photo", "user")


class CompletedCoursesAdmin(admin.ModelAdmin):
    list_display = ("id", "user_in_current_course", "current_course", "course_done")



admin.site.register(CompletedCourse,CompletedCoursesAdmin)
#admin.site.register(Users)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Courses, CoursesAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(CompletedTasks, CompletedTasksAdmin)
