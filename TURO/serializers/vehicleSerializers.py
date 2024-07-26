from TURO.models import Feature, Vehicle
from rest_framework import serializers

from rest_framework.exceptions import ValidationError
from ..models import VehicleImages


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class VehicleDetails(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
            "id",
            "category",
            "make",
            "model",
            "thumbnail",
            "engine_capacity",
            "transmission",
            "year",
            "fuel_type",
            "created_at",
            "updated_at",
            "registration_document",
            "insurance_document",
            "owner",
            "features",
        ]

    def get_thumbnail(self, obj):
        images = VehicleImages.objects.filter(vehicle=obj)
        for image in images:
            if image.thumbnail_image:
                return image.thumbnail_image.url
        return None


class VehicleBasicDetailsSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
            "id",
            "category",
            "make",
            "model",
            "thumbnail",
            "engine_capacity",
            "transmission",
            "year",
            "fuel_type",
            "created_at",
            "updated_at",
            "registration_document",
            "insurance_document",
            "owner",
            "features",
        ]

    def get_thumbnail(self, obj):
        images = VehicleImages.objects.filter(vehicle=obj)
        for image in images:
            if image.thumbnail_image:
                return image.thumbnail_image.url
        return None

    def create(self, validated_data):
        # Extract features data
        features_data = validated_data.pop("features")

        # Check if the vehicle already exists for the user
        owner = validated_data["owner"]
        category = validated_data["category"]
        make = validated_data["make"]
        model = validated_data["model"]
        year = validated_data["year"]
        engine_capacity=validated_data["engine_capacity"]
        transmission=validated_data["transmission"]
        fuel_type = validated_data["fuel_type"]

        existing_vehicle = Vehicle.objects.filter(
            owner=owner,
            category=category,
            make=make,
            model=model,
            year=year,
            engine_capacity=engine_capacity,
            transmission=transmission,
            fuel_type=fuel_type,
        ).first()

        if existing_vehicle:
            raise ValidationError(
                "A vehicle with similar data already exists for the user."
            )

        # Create the new vehicle
        vehicle = Vehicle.objects.create(**validated_data)

        # Handle features
        for feature_data in features_data:
            feature, created = Feature.objects.get_or_create(name=feature_data["name"])
            vehicle.features.add(feature)

        return vehicle


class VehicleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["registration_document", "insurance_document"]


class UpdateVehicleBasicDetailsSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)

    class Meta:
        model = Vehicle
        fields = [
            "make",
            "model",
            "engine_capacity",
            "transmission",
            "year",
            "fuel_type",
            "features",
        ]

    def update(self, instance, validated_data):
        features_data = validated_data.pop("features")

        # Update the Vehicle instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update features
        instance.features.clear()
        for feature_data in features_data:
            feature, created = Feature.objects.get_or_create(name=feature_data["name"])
            instance.features.add(feature)

        return instance


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImages
        fields = ["vehicle_image"]


class UploadVehicleImagesSerializer(serializers.Serializer):
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())
    thumbnail = serializers.ImageField(write_only=True, required=False)
    images = serializers.ListField(
        child=serializers.ImageField(max_length=100000), write_only=True
    )
