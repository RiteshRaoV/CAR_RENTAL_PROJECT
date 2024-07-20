import random
from rest_framework import serializers

from rest_framework.exceptions import ValidationError
from ..models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["vehicle", "user", "start_date", "end_date"]

    def create(self, validated_data):
        vehicle = validated_data["vehicle"]
        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]

        # Calculate the number of days
        num_days = (end_date - start_date).days
        total_price = num_days * vehicle.price_per_day

        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)
        # Check if the vehicle is available
        if not vehicle.availability:
            raise ValidationError("The vehicle is not available for reservation.")
        # Create the reservation
        reservation = Reservation.objects.create(
            vehicle=vehicle,
            user=validated_data["user"],
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status="pending",
            otp=otp,
        )

        # Set vehicle availability to false
        vehicle.availability = False
        vehicle.save()

        return reservation


class ApproveReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    otp = serializers.CharField(max_length=6)


class UserReservationSerializer(serializers.ModelSerializer):
    vehicle_make = serializers.CharField(source="vehicle.make")
    vehicle_model = serializers.CharField(source="vehicle.model")
    vehicle_id = serializers.IntegerField(source="vehicle.id")

    class Meta:
        model = Reservation
        fields = [
            "id",
            "vehicle_id",
            "vehicle_make",
            "vehicle_model",
            "user",
            "start_date",
            "end_date",
            "status",
        ]


class VehicleReservationSerializer(serializers.ModelSerializer):
    vehicle_make = serializers.CharField(source="vehicle.make")
    vehicle_model = serializers.CharField(source="vehicle.model")
    vehicle_id = serializers.IntegerField(source="vehicle.id")
    reservation_id = serializers.IntegerField(source="id")

    class Meta:
        model = Reservation
        fields = [
            "reservation_id",
            "vehicle_id",
            "vehicle_make",
            "vehicle_model",
            "user",
            "start_date",
            "end_date",
            "total_price",
            "status",
        ]
