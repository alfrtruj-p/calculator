from django import forms
from .models import Input


class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        fields = ['customer_name', 'piqlConnect_1TB_120GB_in_EUR_per_yr', 'online_data_in_GB', 'online_sales_price_EUR_per_GB',
                  'offline_data_in_GB', 'offline_sales_price_EUR_per_GB', 'comment', 'created_date']