# Generated by Django 3.2.3 on 2021-05-27 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0029_auto_20210526_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, unique=True),
        ),
    ]
