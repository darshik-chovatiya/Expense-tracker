from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=20 , unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
    
class Category(models.Model):

    name = models.CharField(max_length=50)
    user = models.ForeignKey(Users , on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Expense(models.Model):

    user = models.ForeignKey(Users , on_delete=models.CASCADE)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    other = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.title


