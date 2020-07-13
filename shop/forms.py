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
    name = forms.CharField(label="Ваше имя", max_length=100,
                           widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    email = forms.CharField(label='email', required=False, widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    phone = forms.IntegerField(label='Номер телефона', required=False)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-control'}))


SEX_CHOISES = [
    ('муж', 'Муж'),
    ('жен', 'Жен'),
]

OBJECTIVE_CHOISES = [
    ('Набрать массу', 'Набрать массу'),
    ('Похудеть', 'Похудеть'),
    ('Поддержать форму', 'Поддержать форму'),
]
NUMBER_OF_MEALS = [
    ('3', '3'),
    ('1', '1'),
    ('2', '2'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
]


class CalcForm(forms.Form):
    sex = forms.ChoiceField(label="Выберете пол", choices=SEX_CHOISES)
    year = forms.IntegerField(label="Сколько Вам лет?", max_value=80, min_value=10)
    height = forms.IntegerField(label="Какой у Вас рост?", max_value=220, min_value=100)
    body_mass = forms.IntegerField(label="Укажите массу тела", max_value=200, min_value=30)
    number_of_meals = forms.ChoiceField(label="Сколько раз в день Вы питаетесь?", choices=NUMBER_OF_MEALS)
    objective = forms.ChoiceField(label="Выберете Вашу цель", choices=OBJECTIVE_CHOISES)


class EmailForm(forms.Form):
    email = forms.Field()
