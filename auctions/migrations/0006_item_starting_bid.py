# Generated by Django 5.1.1 on 2024-09-19 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_item_description_alter_item_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default=50, max_digits=10),
            preserve_default=False,
        ),
    ]
