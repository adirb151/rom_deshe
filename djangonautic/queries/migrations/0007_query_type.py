# Generated by Django 3.2.13 on 2022-05-14 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '0006_alter_query_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='type',
            field=models.CharField(default='Server', max_length=20),
        ),
    ]
