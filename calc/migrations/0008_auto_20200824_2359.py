# Generated by Django 3.0.8 on 2020-08-24 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0007_auto_20200823_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input',
            name='awa_contribution',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=40, verbose_name='Entity'),
        ),
        migrations.AlterField(
            model_name='input',
            name='awa_storage',
            field=models.CharField(choices=[('5', '5 years'), ('10', '10 years'), ('25', '25 years')], default='5', max_length=40, verbose_name='AWA Storage'),
        ),
    ]