# Generated by Django 4.2.5 on 2024-01-19 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='receipt_image',
            field=models.ImageField(blank=True, default='default_receipt.jpg', null=True, upload_to='receipts/'),
        ),
    ]
