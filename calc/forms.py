from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User
from .models import Input


class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        PAY = [('yearly', 'Yearly'), ('monthly', 'Monthly'), ('only_piqlfilm', 'Only piqlFilm')]
        TYPE = [('digital', 'Digital'), ('visual', 'Visual'), ('hybrid', 'Hybrid')]
        LAYOUT = [('1', '1 page'), ('2', '2 pages'), ('3', '3 pages'), ('4', '4 page'), ('6', '6 pages'),
                  ('10', '10 pages')]
        type = forms.ChoiceField(widget=forms.Select(choices=TYPE))
        layout = forms.ChoiceField(widget=forms.Select(choices=LAYOUT))
        payment = forms.ChoiceField(widget=forms.Select(choices=PAY))
        comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
        fields = ['customer_name', 'offline_data', 'type', 'pages', 'layout', 'online_data', 'payment',
                  'comment']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Signup', 'Signup', css_class='btn btn-primary'))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')