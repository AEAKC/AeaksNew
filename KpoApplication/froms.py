from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from KpoApplication.models import Users


class RegisterUserFrom(UserCreationForm):

    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input1'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input1'}))
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(attrs={'class': 'form-input1'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-input1'}))
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input1'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input1'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input1'}),
            'email': forms.EmailInput(attrs={'class': 'form-input1'})


        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-input2'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input3'}))


class UserPhoto(forms.ModelForm):
    photo = forms.FileInput(attrs={'class':'custom-file-input',"name":"image" })
    class Meta:
        model=Users
        fields=('photo',)