# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForm,CustomUserCreationForm
from .models import PupilProfile, TeacherProfile
from django.contrib.auth import logout

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