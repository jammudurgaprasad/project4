# Generated by Django 5.1.1 on 2024-10-16 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop4', '0012_cartitem_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='biryani',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
