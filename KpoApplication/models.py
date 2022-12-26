from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    photo = models.ImageField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_course = models.ForeignKey('Courses', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Доп.пользователь"
        verbose_name_plural = "Доп.пользователи"


class Exercise(models.Model):
    task_number = models.IntegerField(verbose_name="Номер задачи")
    title = models.CharField(max_length=100, verbose_name="Название задачи")
    task_text = models.CharField(max_length=1000, verbose_name="Текст задачи")
    course = models.ForeignKey("Courses", on_delete=models.CASCADE, default=None, verbose_name="Курс")
    blocks = models.ForeignKey("Block", on_delete=models.CASCADE, default=None, verbose_name="Блок", null=True,
                               blank=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title


class Block(models.Model):
    number_of_block = models.CharField(blank=True, null=True, verbose_name="Номер блока", max_length=255)
    title = models.CharField(verbose_name="Название блока", max_length=255, null=True, blank=True)
    course = models.ForeignKey("Courses", verbose_name="Курс", on_delete=models.CASCADE, null=True, blank=True)
    ex = models.ManyToManyField("Exercise", blank=True, null=True)

    class Meta:
        verbose_name = "Блок"
        verbose_name_plural = "Блоки"

    def __str__(self):
        return self.title


class Test(models.Model):
    test_input = models.CharField(max_length=255)
    for_task = models.ForeignKey(to="Exercise", on_delete=models.CASCADE, verbose_name="К задаче")
    expected_output = models.CharField(max_length=255, verbose_name="Ожидаемый ввод")
    is_exception = models.BooleanField(default=False, verbose_name="Ошибка")

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return f"Тест к задаче {self.for_task.title}"


class CompletedTasks(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    exercise = models.ForeignKey(to="Exercise", verbose_name="Задача", on_delete=models.CASCADE)
    correct = models.BooleanField(default=False, verbose_name="Правильность выполнения")

    class Meta:
        verbose_name = "Выполненая задача"
        verbose_name_plural = "Выполненые задачи"

    def __str__(self):
        return f"{self.user.username}, {self.exercise.title}"


class Courses(models.Model):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    DIFFICULTY_CHOICES = [
        (EASY, "Простая"),
        (MEDIUM, "Средняя"),
        (HARD, "Сложная"),
    ]
    number_of_course = models.SmallIntegerField(null=True, blank=True, verbose_name="Номер курса")
    title = models.CharField(max_length=255, verbose_name="Загловок")
    text = models.TextField(max_length=1000, verbose_name="Текст")
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, default=None, max_length=255, verbose_name="Сложность")
    blocks = models.ManyToManyField(Block, verbose_name="Блоки")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class CompletedCourse(models.Model):
    user_in_current_course = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                               verbose_name="Пользователь")
    current_course = models.ForeignKey("Courses", on_delete=models.CASCADE, verbose_name="Текущий курс", null=True,
                                       blank=True)
    course_done = models.BooleanField(default=False, verbose_name="Курс пройден")

    class Meta:
        verbose_name = "Законченый курс"
        verbose_name_plural = "Законченные курсы"

    def __str__(self):
        return f"Курс: {self.current_course.title}"
