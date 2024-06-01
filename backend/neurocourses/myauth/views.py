# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForm,CustomUserCreationForm
from .models import PupilProfile, TeacherProfile
from django.contrib.auth import logout
from .forms import CustomUserChangeForm, PupilProfileForm, TeacherProfileForm
from .models import CustomUser, PupilProfile, TeacherProfile

def login_view(request):
    error_messages = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Замените 'home' на имя вашего URL
            else:
                error_messages.append("Неправильный email или пароль.")
        else:
            error_messages.extend(form.errors.values())
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error_messages': error_messages})

def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data['user_type']
            if user_type == 'pupil':
                PupilProfile.objects.create(user=user)
            elif user_type == 'teacher':
                TeacherProfile.objects.create(user=user)
            login(request, user)
            return redirect('login')  # Change 'home' to your desired redirect URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile_view(request, section='profile'):
    user = request.user
    if hasattr(user, 'pupil_profile'):
        profile = user.pupil_profile
        profile_form_class = PupilProfileForm
    elif hasattr(user, 'teacher_profile'):
        profile = user.teacher_profile
        profile_form_class = TeacherProfileForm
    else:
        profile = None
        profile_form_class = None

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        if profile:
            profile_form = profile_form_class(request.POST, instance=profile)
        if user_form.is_valid() and (not profile or profile_form.is_valid()):
            user_form.save()
            if profile:
                profile_form.save()
            return redirect('profile', section='profile')
    else:
        user_form = CustomUserChangeForm(instance=user)
        if profile:
            profile_form = profile_form_class(instance=profile)
        else:
            profile_form = None

    templates = {
        'profile': 'lk_edit.html',
        'photo': 'lk_photo.html',
        'purchased_courses': 'lk_purchased_courses.html',
        'favorite_courses': 'lk_favorite_courses.html',
    }

    template = templates.get(section, 'lk_edit.html')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'template': template,
    }
    return render(request, 'profile.html', context)