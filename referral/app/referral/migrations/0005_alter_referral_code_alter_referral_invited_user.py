# Generated by Django 4.2.3 on 2023-07-17 20:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('referral', '0004_alter_referral_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='code',
            field=models.CharField(default='3362bd', editable=False, max_length=6, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='referral',
            name='invited_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referrals', to=settings.AUTH_USER_MODEL),
        ),
    ]
