from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

STATUS_CHOICES =[
    ('created', 'created'),
    ('started', 'started'),
    ('completed', 'completed')
]


class PhoneBook(models.Model):
    agent = models.CharField(max_length=255, default='admin')
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    created_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.name


class Contact(models.Model):
    agent = models.CharField(max_length=255, default='admin')
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    created_date = models.DateTimeField(default=datetime.now())
    phone_number = models.IntegerField(unique=True)
    phone_book = models.ForeignKey(PhoneBook, on_delete=models.CASCADE)

    def __str__(self):
        return self.phone_number


class Campaign(models.Model):
    agent = models.CharField(max_length=255, default='admin')
    name = models.CharField(max_length=255, default='')
    text_speech = models.TextField(default='')
    phone_book = models.ForeignKey(PhoneBook, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='created', choices=STATUS_CHOICES)
    creation_date = models.DateTimeField(default=datetime.now())
    started_date = models.DateTimeField(blank=True, editable=True, null=True)

    def __str__(self):
        return self.name


class Call(models.Model):
    agent = models.CharField(max_length=255, default='admin')
    start_date = models.DateTimeField(default=datetime.now())
    duration = models.IntegerField()
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    cost = models.IntegerField()
