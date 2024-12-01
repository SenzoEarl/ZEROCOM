# Generated by Django 5.1.3 on 2024-11-06 05:58

import main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_question_answer_quiz_question_quiz_quizresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lottery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('number', models.IntegerField(default=main.models.genNumber)),
                ('description', models.TextField(default='Enter what it means', max_length=250)),
            ],
        ),
    ]