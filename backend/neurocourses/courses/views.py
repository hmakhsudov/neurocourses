from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Course, Chapter, Lesson, Category

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')



def courses(request):
    all_courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': all_courses})

def course_search(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(title__icontains=query)
    else:
        courses = Course.objects.all()
    return render(request, 'courses_search.html', {'courses': courses, 'query': query})

def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    chapters = Chapter.objects.filter(course=course).order_by('chapter_index')
    lessons = {chapter: Lesson.objects.filter(chapter=chapter).order_by('lesson_index') for chapter in chapters}  
    lessons_dict = {chapter: Lesson.objects.filter(chapter=chapter) for chapter in chapters}
    # Подсчет количества видео лекций и текстовых документов
    video_lectures_count = sum(lesson.lesson_type == 'video' for chapter in chapters for lesson in lessons_dict[chapter])
    text_documents_count = sum(lesson.lesson_type == 'text' for chapter in chapters for lesson in lessons_dict[chapter])
    categories = course.category.all()

    context = {
        'course': course,
        'chapters': chapters,
        'lessons': lessons,
        'categories': categories,
        'video_lectures_count': video_lectures_count,
        'text_documents_count': text_documents_count,
    }
    return render(request, 'course_details.html', context)