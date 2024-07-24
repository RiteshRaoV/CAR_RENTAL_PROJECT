from tkinter import CASCADE
from django.db import models
from django.conf import settings
from TURO.models import Vehicle

# Create your models here.
class Listing(models.Model):
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE,related_name="listings")
    listing_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    mileage = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    ad_status = models.CharField(max_length=20,choices=[
        ('sold','Sold'),
        ('pending','Pending'),
        ('for sale','For Sale')
    ],default='For Sale')
    condition = models.CharField(max_length=10,choices=[
        ('used','Used'),
        ('new','New')
    ])
    description = models.TextField(max_length=200)
    
    def __str__(self):
        return f'{self.vehicle.make}-{self.price}'
    
    
class InterestRequest(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected')
    ]
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="requests")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="requests")
    request_price = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')
    request_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Interest request from {self.buyer} for listing {self.listing} - {self.status}"