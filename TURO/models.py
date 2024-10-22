from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator,RegexValidator
import random
import string


class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    profile_picture = models.ImageField(upload_to="profile-pics/",blank=True,null=True)
    aadhar_image = models.ImageField(upload_to="aadhar/", blank=True, null=True)
    dl_image = models.ImageField(upload_to="dl/", blank=True, null=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Contact number must be exactly 10 digits.',
                code='invalid_contact_number'
            )
        ]
    )
    def __str__(self):
        return f"Profile of {self.user.username}"


class Vehicle(models.Model):
    TRANSMISSION_CHOICES = [
        ('manual','Manual'),
        ('automatic','Automatic')
    ]
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vehicles"
    )
    category = models.CharField(max_length=10)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    engine_capacity = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10000)]
    )
    transmission = models.CharField(max_length=25,choices=TRANSMISSION_CHOICES,default=None)
    year = models.IntegerField(default=0)
    fuel_type = models.CharField(max_length=10)
    features = models.ManyToManyField(Feature, related_name="vehicles", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registration_document = models.ImageField(
        upload_to="vehicle_docs/", blank=True, null=True
    )
    insurance_document = models.ImageField(
        upload_to="vehicle_docs/", blank=True, null=True
    )

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class RentListing(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="rent_listings")
    listing_date = models.DateField(auto_now_add=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    
    def __str__(self):
        return f"{self.vehicle.make} - {self.price_per_day} per day"
    
class VehicleImages(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="images", default=None
    )
    thumbnail_image = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    vehicle_image = models.ImageField(upload_to="vehicle_image/", blank=True, null=True)


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    rental_listing  = models.ForeignKey(
        RentListing, on_delete=models.CASCADE, related_name="reservations"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"Reservation {self.id} for {self.rental_listing.vehicle}"

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_otp()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_otp():
        return "".join(random.choices(string.digits, k=6))


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} by {self.user}"
