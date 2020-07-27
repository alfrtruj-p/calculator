from django.db import models
from django.utils import timezone
from calc import calculator
# Create your models here.


class Input(models.Model):
    partner_name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=40)
    piqlConnect_1TB_120GB_in_EUR_per_yr = models.FloatField(default=calculator.piqlConnect_bundle)
    online_data_in_GB = models.FloatField()
    online_sales_price_EUR_per_GB = models.FloatField(default=calculator.online_price)
    offline_data_in_GB = models.FloatField()
    offline_sales_price_EUR_per_GB = models.FloatField(default=calculator.offline_price)
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.customer_name





