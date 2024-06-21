# Generated by Django 4.1 on 2024-05-07 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0003_delete_final_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cartitems',
        ),
        migrations.AddField(
            model_name='order',
            name='order_pic',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='pro_name',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]