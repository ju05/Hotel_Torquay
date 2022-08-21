# Generated by Django 2.2.5 on 2022-08-18 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('category', models.CharField(choices=[('STA', 'STANDARD'), ('COS', 'COSY'), ('FAM', 'FAMILY'), ('PRE', 'PREMIUM'), ('LUX', 'DELUXE')], max_length=3)),
                ('beds', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitor.Room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]