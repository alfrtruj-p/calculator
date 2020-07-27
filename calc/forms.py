from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User

from .models import Input


class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        fields = ['customer_name', 'piqlConnect_1TB_120GB_in_EUR_per_yr', 'online_data_in_GB', 'online_sales_price_EUR_per_GB',
                  'offline_data_in_GB', 'offline_sales_price_EUR_per_GB', 'comment', 'created_date']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Signup', 'Signup', css_class='btn btn-primary'))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')