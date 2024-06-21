# Generated by Django 4.1 on 2024-05-07 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Addressdetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=200)),
                ('address_line2', models.CharField(max_length=200)),
                ('pincode', models.IntegerField()),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('contact_name', models.CharField(max_length=20)),
                ('contact_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='cartitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('selectedsize', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ecomregister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propic', models.ImageField(upload_to='images/')),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='sellerproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productimage', models.ImageField(upload_to='images/')),
                ('product', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('size', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='final_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchased_date', models.DateField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerceapp.addressdetails')),
                ('cart_items', models.ManyToManyField(to='ecommerceapp.cartitem')),
                ('userdetails', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerceapp.ecomregister')),
            ],
        ),
        migrations.AddField(
            model_name='cartitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerceapp.sellerproduct'),
        ),
        migrations.AddField(
            model_name='addressdetails',
            name='userdetails',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerceapp.ecomregister'),
        ),
    ]