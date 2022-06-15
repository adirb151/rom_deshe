from django.db import models
from datetime import datetime, timedelta


def expire():
    return datetime.now() + timedelta(days=3)

def current_date():
    return datetime.datetime.now()

    


class Query(models.Model):
    name = models.CharField(max_length=20, default="Unknown")
    data = models.CharField(max_length=200)
    slug = models.SlugField()
    status = models.CharField(default="Running", max_length=10)
    date = models.DateTimeField(default=datetime.now)
    expiration_date = models.DateTimeField(default=expire)
    log = models.TextField(max_length=20000, default="", blank=True)
    prediction = models.CharField(default="Not yet", max_length=20000)
    type = models.CharField(default="Server", max_length=20)
    
    def print_log(self):
        return self.log

    def __str__(self):
        return self.data[:20]

    def is_past_due(self):
        return datetime.now() > self.expiration_date.replace(tzinfo=None)

    def duration(self):
        return datetime.now() - self.date.replace(tzinfo=None) + timedelta(hours=3)