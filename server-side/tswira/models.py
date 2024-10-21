from django.db import models
from djstripe.models import Customer
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from storages.backends.s3boto3 import S3Boto3Storage

class UserProfileT(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer = models.CharField(max_length=255, blank=True, null=True)

class WaitListT(models.Model):
    email = models.EmailField(unique=True)
    source = models.CharField(max_length=100, null=True, blank=True)    
    ip = models.CharField(max_length=100, null=True, blank=True)

class GoogleProfileT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    uid = models.CharField(blank=True, null=True, max_length=255, unique=True)
    profile = models.CharField(max_length=255, default="https://www.gravatar.com/avatar/?d=mp")

class SubscriptionT(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default="inactive")
    plan = models.CharField(
        max_length=255,
        default="free",
        choices=[("free", "Free"), ("starter", "Starter"), ("pro", "Pro")],
    )
    stripe_subscription_id = models.CharField(
        max_length=255, null=True, blank=True, default=None
    )

class FeaturesT(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tokens = models.FloatField(
        default=0
    )
     
    token_limits = models.IntegerField(
        default=settings.PRICINGS["free"]["tokens_limits"]
    )
    images =  models.FloatField(
        default=0
    )

    images_limits = models.IntegerField(
        default=settings.PRICINGS["free"]["images_limits"]
    )

class UserImageT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/', storage=default_storage, verbose_name=_("User Image"))
    created_at = models.DateTimeField(auto_now_add=True)

class GeneratedPhotoT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user_token = models.TextField(blank=True, null=True)
    prompt = models.TextField()
    style_name = models.TextField()
    num_outputs = models.IntegerField(default=1)
    input_images = models.TextField(blank=True, null=True)
    is_free = models.BooleanField(default=True, null=True)

    image = models.TextField(blank=True, null=True)
    job_id = models.TextField(blank=True, null=True)
    status = models.CharField(blank=True, default="pending", null=True, max_length=255)
    key = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s Generated Photo"