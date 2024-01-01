# Generated by Django 4.2.2 on 2023-10-07 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stock',
            field=models.CharField(choices=[('in stock', 'IN STOCK'), ('low stock', 'LOW STOCK'), ('out of stock', 'OUT OF STOCK')], default='out of stock', max_length=20),
        ),
        migrations.AlterField(
            model_name='item',
            name='unit',
            field=models.CharField(choices=[('unit', 'Unit'), ('stack', 'Stack')], default='unit', max_length=20),
        ),
    ]
