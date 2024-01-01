# Generated by Django 4.2.2 on 2023-10-07 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images/')),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('unit', models.CharField(choices=[('unit', 'Unit'), ('stack', 'Stack')], default='unit', max_length=200)),
            ],
        ),
    ]