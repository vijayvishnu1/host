# Generated by Django 4.1.1 on 2023-03-30 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_filed_lawsuits_cnr_filed_lawsuits_court_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='filed_lawsuits',
            name='judges',
            field=models.ManyToManyField(blank=True, to='accounts.judge'),
        ),
    ]
