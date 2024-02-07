# Generated by Django 5.0 on 2024-02-07 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfe_app', '0007_alter_addvideomodel_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addvideomodel',
            name='video',
            field=models.FileField(upload_to='videos/'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
