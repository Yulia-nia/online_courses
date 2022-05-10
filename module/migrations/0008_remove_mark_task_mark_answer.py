# Generated by Django 4.0.3 on 2022-05-08 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0007_task_studentanswer_mark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mark',
            name='task',
        ),
        migrations.AddField(
            model_name='mark',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='module.studentanswer'),
        ),
    ]