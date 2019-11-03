# Generated by Django 2.2.6 on 2019-11-01 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ap', models.CharField(max_length=63, unique=True, verbose_name='ap')),
                ('max', models.PositiveIntegerField(verbose_name='max')),
                ('current', models.PositiveIntegerField(verbose_name='current')),
                ('min', models.PositiveIntegerField(verbose_name='min')),
                ('avg', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='avg')),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name='timestamp')),
            ],
        ),
    ]