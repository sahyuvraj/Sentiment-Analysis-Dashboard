from django.db import models

class Review(models.Model):
    content = models.TextField()
    sentiment = models.CharField(max_length=10)
