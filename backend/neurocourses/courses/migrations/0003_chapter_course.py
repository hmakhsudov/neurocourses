# Generated by Django 5.0.6 on 2024-05-17 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.course', verbose_name='Курс'),
            preserve_default=False,
        ),
    ]
