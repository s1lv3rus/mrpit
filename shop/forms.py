from django import forms
from .models import Comment


class SearchForm(forms.Form):
    query = forms.CharField()


class AddComment(forms.ModelForm):
    body = forms.Textarea()

    class Meta:
        model = Comment
        fields = ['body']


class ContactForm(forms.Form):
    subject = forms.CharField(label="Тема:", max_length=100, widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    message = forms.CharField(label='Сообщение',  widget=forms.Textarea(attrs={'class': 'form-control'}))