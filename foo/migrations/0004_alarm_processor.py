# Generated by Django 2.2.4 on 2022-07-10 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foo', '0003_auto_20220710_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='processor',
            field=models.BigIntegerField(null=True),
        ),
    ]
