from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User
from .models import Input


class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        PAY = [('yearly', 'Yearly'), ('monthly', 'Monthly'), ('only_piqlfilm', 'Only piqlFilm'), ('only_piqlreader', 'Only piqlReader')]
        TYPE = [('digital', 'Digital'), ('visual', 'Visual'), ('hybrid', 'Hybrid')]
        LAYOUT = [('1', '1 page'), ('2', '2 pages'), ('3', '3 pages'), ('4', '4 page'), ('6', '6 pages'),
                  ('10', '10 pages')]
        CONTRIBUTION = [('public', 'Public'), ('private', 'Private')]
        STORAGE = [('5', '5 years'), ('10', '10 years'), ('25', '25 years')]
        DECISION = [('yes', 'Yes'), ('no', 'No')]
        SERVICE = [('platinum', 'Platinum'), ('gold', 'Gold')]
        type = forms.ChoiceField(widget=forms.Select(choices=TYPE))
        layout = forms.ChoiceField(widget=forms.Select(choices=LAYOUT))
        payment = forms.ChoiceField(widget=forms.Select(choices=PAY))
        awa = forms.ChoiceField(widget=forms.Select(choices=DECISION))
        awa_contribution = forms.ChoiceField(widget=forms.Select(choices=CONTRIBUTION))
        awa_storage = forms.ChoiceField(widget=forms.Select(choices=STORAGE))
        piqlreader = forms.ChoiceField(widget=forms.Select(choices=DECISION))
        service = forms.ChoiceField(widget=forms.Select(choices=SERVICE))
        consultancy = forms.ChoiceField(widget=forms.Select(choices=DECISION, attrs={'onchange': 'disableProf_serv()'}))
        comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
        fields = ['customer_name', 'type', 'offline_data', 'pages', 'layout', 'online_data', 'payment',
                  'awa', 'awa_contribution', 'awa_storage', 'piqlreader', 'quantity', 'service', 'consultancy', 'days', 'comment']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Signup', 'Signup', css_class='btn btn-primary'))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')