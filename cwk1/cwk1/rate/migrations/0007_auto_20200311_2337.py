# Generated by Django 3.0.4 on 2020-03-11 23:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rate', '0006_auto_20200311_2337'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='professorrating',
            unique_together={('professor', 'module_state', 'user', 'rating')},
        ),
    ]
