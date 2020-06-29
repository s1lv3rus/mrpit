from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    # регулярка только на латиницу
    # username = forms.RegexField(label='Логин', regex='^[a-zA-Z0-9]+$', error_messages={'invalid': ("Только символы "
    #                                                                                                "латинского "
    #                                                                                                "алфавита ")})
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Email для отправки чека')

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'city', 'address', 'postal_code', 'phone')
