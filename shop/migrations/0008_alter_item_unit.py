# Generated by Django 4.2.2 on 2023-10-08 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_item_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='unit',
            field=models.CharField(blank=True, choices=[('', ''), ('unit', 'Unit'), ('stack', 'Stack')], max_length=20, null=True),
        ),
    ]
