from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Hashed
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_full_name(self):
        return f"{self.first_name or self.email}".strip()

    def __str__(self):
        return self.get_full_name()
