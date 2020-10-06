from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User
from .models import Input, DECISION, TYPE


class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        fields = ['customer_name', 'type', 'offline_data', 'pages', 'layout', 'online_data', 'payment',
                  'awa', 'awa_contribution', 'awa_storage', 'piqlreader', 'quantity', 'service', 'consultancy',
                  'days', 'production', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['type'] = forms.ChoiceField(
            choices=TYPE,
            widget=forms.Select(attrs={'onchange': 'disableStorage()'})
        )
        self.fields['offline_data'].required = False
        self.fields['pages'].required = False
        self.fields['layout'].required = False
        self.fields['awa'] = forms.ChoiceField(
            choices=DECISION,
            widget=forms.Select(attrs={'onchange': 'disableAwa()'})
        )
        self.fields['awa_contribution'].required = False
        self.fields['awa_storage'].required = False
        self.fields['piqlreader'] = forms.ChoiceField(
            choices=DECISION,
            widget=forms.Select(attrs={'onchange': 'disableReader()'})
        )
        self.fields['quantity'].required = False
        self.fields['service'].required = False
        self.fields['consultancy'] = forms.ChoiceField(
            choices=DECISION,
            widget=forms.Select(attrs={'onchange': 'disableProf_serv()'})
        )
        self.fields['days'].required = False


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Signup', 'Signup', css_class='btn btn-primary'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

