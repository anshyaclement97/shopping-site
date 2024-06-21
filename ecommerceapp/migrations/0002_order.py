# Generated by Django 4.1 on 2024-05-07 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerceapp.addressdetails')),
                ('cartitems', models.ManyToManyField(to='ecommerceapp.cartitem')),
                ('userdetails', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerceapp.ecomregister')),
            ],
        ),
    ]