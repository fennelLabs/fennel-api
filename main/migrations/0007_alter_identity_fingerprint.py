# Generated by Django 4.0.5 on 2022-06-22 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_identity_fingerprint_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identity',
            name='fingerprint',
            field=models.CharField(max_length=256),
        ),
    ]
