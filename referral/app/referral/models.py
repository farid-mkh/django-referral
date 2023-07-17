import uuid
from django.db import models
from user.models import User

# Create your models here.
class Referral(models.Model):
    code = models.CharField(
        primary_key=True,
        max_length=6,
        default=uuid.uuid4().hex[:6],
        editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    invited_user = models.ManyToManyField(User,related_name='referrals',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code