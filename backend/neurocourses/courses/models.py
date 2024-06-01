from django.db import models
from django.urls import reverse
from myauth.models import TeacherProfile
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings



class Category(models.Model):
    name = models.CharField(_("Название"), max_length=50)
    category_image = models.ImageField(_("Картинка"), upload_to='categories/')

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})


class Chapter(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название части')
    chapter_index = models.PositiveIntegerField(verbose_name='Порядковый номер')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')
    
    def __str__(self):
        return self.name


class Lesson(models.Model):
    VIDEO_LECTURE = 'video'
    TEXT_ASSIGNMENT = 'text'

    LESSON_TYPE_CHOICES = [
        (VIDEO_LECTURE, 'Видео лекция'),
        (TEXT_ASSIGNMENT, 'Текстовое задание'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название урока', null=True, default='none')
    lesson_index = models.PositiveIntegerField(verbose_name='Порядковый номер', default=1)
    file = models.FileField(verbose_name='Файл', null=True, blank=True, upload_to='files/')
    video_url = models.URLField(verbose_name='Ссылка на видео', null=True, blank=True)
    chapter = models.ForeignKey('Chapter', verbose_name='Глава', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lesson_type = models.CharField(
        max_length=5,
        choices=LESSON_TYPE_CHOICES,
        default=VIDEO_LECTURE,
        verbose_name='Тип занятия'
    )

    def clean(self):
        if self.lesson_type == self.VIDEO_LECTURE and not self.video_url:
            raise ValidationError('Для видео лекции необходимо указать ссылку на видео.')
        if self.lesson_type == self.TEXT_ASSIGNMENT and not self.file:
            raise ValidationError('Для текстового задания необходимо прикрепить файл.')
        if self.lesson_type == self.VIDEO_LECTURE and self.file:
            raise ValidationError('Для видео лекции не нужно прикреплять файл.')
        if self.lesson_type == self.TEXT_ASSIGNMENT and self.video_url:
            raise ValidationError('Для текстового задания не нужно указывать ссылку на видео.')

    def __str__(self):
        return f"{self.name}, номер: {self.lesson_index}"

class Course(models.Model):
    title = models.CharField(max_length=255)
    second_text= models.TextField()
    price = models.IntegerField(_("Цена курса"))
    description = models.TextField()
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category)
    image = models.ImageField(_("Фотография курса"), upload_to='courses/')
    

    

    def __str__(self):
        return self.title
    
    


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
    
    
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    favorited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'

    def __str__(self):
        return f"{self.user.username} favorited {self.course.title}"
    

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"Review by {self.user.username} for {self.course.title}"