import random
from rest_framework import serializers

from rest_framework.exceptions import ValidationError
from ..models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["rental_listing", "user", "start_date", "end_date"]

    def create(self, validated_data):
        rental_listing = validated_data["rental_listing"]
        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]

        # Calculate the number of days
        num_days = (end_date - start_date).days
        total_price = num_days * rental_listing.price_per_day

        # Generate a 6-digit OTP
        otp = "".join(random.choices("0123456789", k=6))

        # Check if the rental listing is available
        if not rental_listing.availability:
            raise ValidationError("The rental listing is not available for reservation.")

        # Create the reservation
        reservation = Reservation.objects.create(
            rental_listing=rental_listing,
            user=validated_data["user"],
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status="pending",
            otp=otp,
        )

        # Set rental listing status to unavailable
        rental_listing.availability = False
        rental_listing.save()

        return reservation


class ApproveReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    otp = serializers.CharField(max_length=6)


class UserReservationSerializer(serializers.ModelSerializer):
    rental_listing_make = serializers.CharField(source="rental_listing.vehicle.make")
    rental_listing_model = serializers.CharField(source="rental_listing.vehicle.model")
    rental_listing_id = serializers.IntegerField(source="rental_listing.id")

    class Meta:
        model = Reservation
        fields = [
            "id",
            "rental_listing_id",
            "rental_listing_make",
            "rental_listing_model",
            "user",
            "start_date",
            "end_date",
            "status",
        ]


class VehicleReservationSerializer(serializers.ModelSerializer):
    rental_listing_make = serializers.CharField(source="rental_listing.vehicle.make")
    rental_listing_model = serializers.CharField(source="rental_listing.vehicle.model")
    rental_listing_id = serializers.IntegerField(source="rental_listing.id")
    reservation_id = serializers.IntegerField(source="id")

    class Meta:
        model = Reservation
        fields = [
            "reservation_id",
            "rental_listing_id",
            "rental_listing_make",
            "rental_listing_model",
            "user",
            "start_date",
            "end_date",
            "total_price",
            "status",
        ]