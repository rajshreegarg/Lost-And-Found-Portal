# Generated by Django 2.2.2 on 2019-06-29 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20190629_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lost_product',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
