# Generated by Django 3.2.3 on 2021-05-19 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20210519_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='high_bid',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
