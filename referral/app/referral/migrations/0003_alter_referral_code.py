# Generated by Django 4.2.3 on 2023-07-17 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0002_alter_referral_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='code',
            field=models.UUIDField(default='38ab37', editable=False, primary_key=True, serialize=False),
        ),
    ]
