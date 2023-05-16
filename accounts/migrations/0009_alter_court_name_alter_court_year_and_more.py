# Generated by Django 4.1.1 on 2023-05-08 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_court_remove_filed_lawsuits_court_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='name',
            field=models.CharField(default='N/A', max_length=255),
        ),
        migrations.AlterField(
            model_name='court',
            name='year',
            field=models.IntegerField(default='N/A'),
        ),
        migrations.AlterField(
            model_name='defendant',
            name='address',
            field=models.CharField(default='N/A', max_length=255),
        ),
        migrations.AlterField(
            model_name='defendant',
            name='email',
            field=models.EmailField(default='N/A', max_length=254),
        ),
        migrations.AlterField(
            model_name='defendant',
            name='name',
            field=models.CharField(default='N/A', max_length=255),
        ),
        migrations.AlterField(
            model_name='defendant',
            name='phone_number',
            field=models.CharField(default='N/A', max_length=20),
        ),
    ]
