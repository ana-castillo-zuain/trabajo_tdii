# Generated by Django 5.0.6 on 2024-06-03 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='Average_Score',
            field=models.FloatField(default=0),
        ),
    ]