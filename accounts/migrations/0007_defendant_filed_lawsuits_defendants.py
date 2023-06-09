# Generated by Django 4.1.1 on 2023-05-08 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_message_delete_chat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Defendant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='filed_lawsuits',
            name='defendants',
            field=models.ManyToManyField(blank=True, to='accounts.defendant'),
        ),
    ]
