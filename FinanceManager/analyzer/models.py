from django.contrib.auth.models import User
from django.db import models
from signup.models import CustomUser
from django.utils.text import slugify
import datetime


class Tag(models.Model):
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag


class Company(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    tag = models.ManyToManyField(Tag)
    image_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='company', blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True, null=True)
    symbol = models.CharField(max_length=20, unique=True)
    days_gap = models.IntegerField(default=60, blank=True, null=True)
    currency = models.CharField(max_length=30, default='INR')
    link = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='data', blank=True, null=True, editable=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    views = models.BigIntegerField(default=0, editable=False)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Master(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.company.name


class Suggestion(models.Model):
    user = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    email = models.EmailField()
    suggestion = models.TextField()

    def __str__(self):
        return self.title


class Complaints(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    complain = models.TextField()

    def __str__(self):
        return self.title
