from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.utils.text import slugify


class CustomUser(User):
    slug = models.SlugField(unique=True, editable=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True, editable=False)
    occupation = models.CharField(max_length=50, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    mobile = models.CharField(max_length=10, blank=True, null=True, error_messages={'error': 'Check the number'})
    profile_image = models.ImageField(upload_to='profile', blank=False, null=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(super(CustomUser, self).username)
        super(CustomUser, self).save(*args, **kwargs)
