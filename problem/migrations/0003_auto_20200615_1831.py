# Generated by Django 2.2.10 on 2020-06-15 12:31

from django.db import migrations, models
import problem.models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0002_auto_20200615_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='output_file',
            field=models.FileField(blank=True, upload_to=problem.models.get_testcase_path),
        ),
    ]
