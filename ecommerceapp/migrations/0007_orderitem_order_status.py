# Generated by Django 4.1 on 2024-05-15 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0006_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order_status',
            field=models.BooleanField(default=True),
        ),
    ]
