from django.contrib.auth import logout
from django.contrib.auth.context_processors import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .froms import RegisterUserFrom, LoginForm, UserPhoto
from .models import *


def main(request):
    return render(request, "html/main.html")


# TODO:Сделать аккаунт пользователя, прикрутить в него статистику, сделать плавные переходы у курсов, прикрутить адаптив

@login_required
def course(request):
    courses = Courses.objects.all()
    print(courses)
    return render(request, "html/courses.html", context={"courses": courses})


def acc(request):
    user_username = request.GET.get("username")
    user_photo = Users.objects.get(user__username=user_username)
    tasks_done = CompletedTasks.objects.filter(user__username=user_username)
    try:
        current_course = Users.objects.get(user__username=user_username).current_course.title
    except AttributeError:
        return render(request, "html/acc.html", context={"user_dop_info": user_photo, "tasks_done": len(tasks_done),
                                                         "current_course": "Вы ещё не проходили курсы на нашем сайте",
                                                         "completed_courses": "0",
                                                         "href_current_course": "/",
                                                         "new_user":"True"})
    for_href_current_course = Users.objects.all().filter(user__username=user_username)
    completed_courses = CompletedCourse.objects.all().filter(user_in_current_course__username=user_username,course_done=True)
    if len(current_course) > 15:
        current_course = current_course[0:15]
        return render(request, "html/acc.html", context={"user_dop_info": user_photo, "tasks_done": len(tasks_done),
                                                         "current_course_short": current_course,
                                                         "completed_courses": len(completed_courses),
                                                         "href_current_course": for_href_current_course})
    else:
        return render(request, "html/acc.html", context={"user_dop_info": user_photo, "tasks_done": len(tasks_done),
                                                         "current_course": current_course,
                                                         "completed_courses": len(completed_courses),
                                                         "href_current_course": for_href_current_course})


def registration(request):
    return render(request, "html/registration.html")


def login(request):
    return render(request, "html/login.html")


@login_required
def task(request):
    tasks = request.GET.get("page")
    courses = request.GET.get("course")
    blocks = request.GET.get("block")
    username = request.GET.get("username")
    try:
        user_in_completed_course = CompletedCourse.objects.get(user_in_current_course__username=username,
                                                               current_course__number_of_course=courses)

        if len(Block.objects.all().filter(course__number_of_course=courses)) == len(
                CompletedTasks.objects.all().filter(user__username=username)) and len(
            CompletedTasks.objects.all().filter(user__username=username)) != 0:
            CompletedCourse.objects.update(course_done=True)

    except:
        user_in_completed_course = CompletedCourse.objects.create(
            user_in_current_course=User.objects.get(username=username),
            current_course=Courses.objects.get(number_of_course=courses), course_done=False)
    ex_list = list(
        i["task_number"] for i in
        Exercise.objects.filter(blocks__id=blocks, course__number_of_course=courses).values(
            "task_number")
    )
    exercise = Exercise.objects.get(blocks__id=blocks, id=tasks, course__number_of_course=courses)

    current_course = Courses.objects.get(number_of_course=courses)
    Users.objects.filter(user__username=username).update(current_course=courses)
    current_block = Block.objects.get(ex__id=tasks, course__number_of_course=courses).id
    paginator = Exercise.objects.all().filter(blocks__id=blocks)
    block = Block.objects.all().filter(course__number_of_course=courses)
    tasks_done = CompletedTasks.objects.filter(user=request.user).values("exercise")
    tasks_wrong = CompletedTasks.objects.filter(user=request.user, correct=False).values("exercise")
    all_tasks_in_course = Exercise.objects.filter(course__number_of_course=courses).values("title")
    if request.method == "POST":
        user_code = request.POST.get("codefield")
        print(user_code)
        tests = Test.objects.filter(for_task=tasks)
        success = True
        for test in tests:
            src = user_code
            print(src)
            try:
                exec(src)
            except Exception as exc:
                success = False
                print(f"compilation exception {exc}")
                break
            try:
                print(f"args={eval(test.test_input)}")
                if str(locals()["f"](eval(test.test_input))) == test.expected_output:
                    continue
                else:
                    print(
                        f'FAILED TEST result:{str(locals()["f"](eval(test.test_input)))} expected: {test.expected_output}'
                    )
                    success = False
                    break
            except Exception as exc:
                if test.is_exception and exc.__class__.__name__ == test.expected_output:
                    print(f"ran test, got expected exception {test.expected_output}")
                    continue
                else:
                    print(f"FAILED TEST result:{exc.__class__.__name__} expected: {test.expected_output}")
                    print(exc)
                    success = False
                    break
        try:
            completed_task = CompletedTasks.objects.get(user=request.user, exercise_id=exercise.id)
        except CompletedTasks.DoesNotExist:
            completed_task = CompletedTasks.objects.create(
                user_id=request.user.id, exercise_id=exercise.id, correct=success
            )
        completed_task.correct = success
        completed_task.save()
        tasks_done = CompletedTasks.objects.filter(user=request.user, correct=True).values("exercise")
        tasks_wrong = CompletedTasks.objects.filter(user=request.user, correct=False).values("exercise")
        return render(
            request,
            "html/task.html",
            context={
                "result": success,
                "title": exercise.title,
                "paginator": paginator,
                "text": exercise.task_text,
                "page": ex_list,
                "current_course": current_course.number_of_course,
                "current_block": current_block,
                "blocks": block,
                "completed_tasks": [i["exercise"] for i in tasks_done],
                "incompleted_tasks": [i["exercise"] for i in tasks_wrong],
            },
        )
    return render(
        request,
        "html/task.html",
        context={
            "title": exercise.title,
            "text": exercise.task_text,
            "page": ex_list,
            "paginator": paginator,
            "current_block": current_block,
            "current_course": current_course.number_of_course,
            "completed_tasks": [i["exercise"] for i in tasks_done],
            "incompleted_tasks": [i["exercise"] for i in tasks_wrong],
            "blocks": block,
        },
    )


@login_required
def courseEasy(request):
    courses = Courses.objects.all().filter(difficulty="EASY")
    return render(request, "html/courses.html", context={"courses_easy": courses})


@login_required
def courseMedium(request):
    courses = Courses.objects.all().filter(difficulty="MEDIUM")
    return render(request, "html/courses.html", context={"courses_medium": courses})


@login_required
def courseHard(request):
    courses = Courses.objects.filter(difficulty="HARD")
    return render(request, "html/courses.html", context={"courses_hard": courses})


class RegisterUser(CreateView):
    form_class = RegisterUserFrom
    template_name = 'html/registration.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'html/login.html'
    def form_valid(self, form):
        get_user = self.request.POST['username']
        try:
            Users.objects.get(user__username=get_user)
        except:
            Users.objects.create(user=User.objects.get(username=get_user),current_course=None,photo=None)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('/')


def courses_done(request):
    username = request.GET.get("username")
    courses_done = CompletedCourse.objects.all().filter(user_in_current_course__username=username, course_done=True)
    print(courses_done)
    return render(request, "html/courses_done.html", context={"completed_courses": courses_done})


def update_profile(request):
    username = request.GET.get('username')
    user_photo = Users.objects.get(user__username=username)
    if "update-photo" in request.POST:
        form = UserPhoto(request.POST, request.FILES)
        print(request.FILES['image'])
        print(".jpg" not in str(request.FILES['image']), ".jgp")
        if ".png" in str(request.FILES['image']) or ".jpg" in str(request.FILES['image']) or ".jpeg" in str(
                request.FILES['image']):
            user_error_upload_file = True
        else:
            user_error_upload_file = False

        if user_error_upload_file:
            if form.is_valid():
                Users.objects.filter(user__username=username).update(photo=request.FILES['image'])
                user_photo = Users.objects.get(user__username=username)
                return render(request, "html/update_profile.html", context={"user_photo": user_photo})
            else:
                print(123)
            return render(request, "html/update_profile.html", context={"user_photo": user_photo})
        else:
            return render(request, "html/update_profile.html",
                          context={"user_photo": user_photo, "error_msg": "Неправильный формат файла"})

    if "update-username-btn" in request.POST:
        current_username = request.POST.get('username')
        new_username = request.POST.get('update-username')
        if len(new_username) < 2:
            return render(request, "html/update_profile.html",
                          context={"user_photo": user_photo,
                                   "username_error": "Имя пользователя не может быть меньше двух символов"})

        User.objects.filter(username=username).update(username=new_username)
        return redirect(f"/update_profile?username={new_username}", context={"user_photo": user_photo})

    if "update-email-btn" in request.POST:
        new_email = request.POST.get('update-email')
        User.objects.filter(username=username).update(email=new_email)
        return render(request, "html/update_profile.html", context={"user_photo": user_photo})
    return render(request, "html/update_profile.html", context={"user_photo": user_photo})

def faq(request):
    return render(request,"html/FAQ.html")