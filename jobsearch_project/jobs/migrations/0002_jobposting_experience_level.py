# Generated by Django 5.2 on 2025-04-23 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobposting',
            name='experience_level',
            field=models.CharField(choices=[('junior', 'Junior'), ('mid', 'Mid-Level'), ('senior', 'Senior')], default='junior', max_length=6),
        ),
    ]
