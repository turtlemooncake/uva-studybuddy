# Generated by Django 4.0.2 on 2022-04-26 22:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('studybuddy', '0012_studysession_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagetwo',
            name='created_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date created'),
        ),
        migrations.AddField(
            model_name='studysession',
            name='created_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date created'),
        ),
    ]
