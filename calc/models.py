from django.db import models
from django.utils import timezone
from calc import calculator
# Create your models here.

PAY = [('yearly', 'Yearly'), ('monthly', 'Monthly'), ('only_piqlfilm', 'Only piqlFilm')]
TYPE = [('digital', 'Digital'), ('visual', 'Visual'), ('hybrid', 'Hybrid')]
LAYOUT = [('1', '1 page'), ('2', '2 pages'), ('3', '3 pages'), ('4', '4 page'), ('6', '6 pages'), ('10', '10 pages')]


class Input(models.Model):
    partner_name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=40, verbose_name='Client')
    offline_data = models.IntegerField(verbose_name='Offline data (GB)', default=0)
    online_data = models.IntegerField(verbose_name='Online data (GB)', default=0)
    type = models.CharField(default='digital', max_length=40, choices=TYPE, verbose_name='Type of preservation', blank=True )
    pages = models.IntegerField(default=0, blank=True, verbose_name='How many pages')
    layout = models.CharField(default='1', blank=True, max_length=40, choices=LAYOUT, verbose_name='Pages per frame')
    payment = models.CharField(max_length=40, choices=PAY)
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.customer_name




