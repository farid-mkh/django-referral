# Generated by Django 4.2.3 on 2023-07-17 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0005_alter_referral_code_alter_referral_invited_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referral',
            name='invited_user',
        ),
        migrations.AlterField(
            model_name='referral',
            name='code',
            field=models.CharField(default='1ecba1', editable=False, max_length=6, primary_key=True, serialize=False),
        ),
    ]
