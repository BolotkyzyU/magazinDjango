# Generated by Django 4.2.6 on 2023-11-09 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.TextField(max_length=255)),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщении',
            },
        ),
    ]