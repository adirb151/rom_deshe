# Generated by Django 4.0.3 on 2022-03-27 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='name',
            field=models.CharField(default='Unknown', max_length=20),
        ),
        migrations.AlterField(
            model_name='query',
            name='status',
            field=models.CharField(default='Running', max_length=10),
        ),
    ]
