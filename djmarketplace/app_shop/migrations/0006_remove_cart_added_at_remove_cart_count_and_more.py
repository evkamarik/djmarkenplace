# Generated by Django 4.0 on 2022-11-07 17:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0002_alter_customer_status'),
        ('app_shop', '0005_alter_cart_added_at_alter_cart_count_alter_cart_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='added_at',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='count',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='item',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='price',
        ),
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='app_users.customer', verbose_name='cart'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='count')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='price')),
                ('added_at', models.DateTimeField(blank=True, null=True, verbose_name='added_at')),
                ('paid_at', models.DateTimeField(blank=True, null=True, verbose_name='paid_at')),
                ('status', models.CharField(default='in_the_cart', max_length=30, verbose_name='status')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='app_users.customer', verbose_name='cart')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_query_name='cart_item', to='app_shop.item', verbose_name='cart')),
            ],
        ),
    ]
