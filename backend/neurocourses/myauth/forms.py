# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, PupilProfile, TeacherProfile


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Адрес электронной почты'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )


class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('pupil', 'Я студент'),
        ('teacher', 'Я преподаватель'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'form-check-input'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите почту'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите Имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите Фамилию'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Повторите пароль'
    }))
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'form-check-input'
    }))
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'user_type')
    
    
    
# forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser, PupilProfile, TeacherProfile

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name']

class PupilProfileForm(forms.ModelForm):
    class Meta:
        model = PupilProfile
        fields = ['date_of_birth']

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['bio', 'expertise']
