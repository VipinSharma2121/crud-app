from django.db import models   # ✅ already present
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
