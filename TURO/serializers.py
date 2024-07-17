from rest_framework import serializers
from .models import Vehicle, Reservation, Review, Feature, UserProfile, VehicleImages


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        fields = "__all__"


class VehicleImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImages
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    features = FeatureSerializer(many=True, read_only=True)
    images = VehicleImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    vehicle = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    vehicle = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = "__all__"
