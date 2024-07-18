from TURO.models import Feature, Vehicle
from rest_framework import serializers

from rest_framework.exceptions import ValidationError


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class VehicleDetails(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class VehicleBasicDetailsSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)

    class Meta:
        model = Vehicle
        fields = "__all__"

    def create(self, validated_data):
        # Extract features data
        features_data = validated_data.pop('features')

        # Check if the vehicle already exists for the user
        owner = validated_data['owner']
        category = validated_data['category']
        make = validated_data['make']
        model = validated_data['model']
        year = validated_data['year']
        price_per_day = validated_data['price_per_day']
        city = validated_data['city']
        address = validated_data['address']
        location = validated_data['location']
        fuel_type = validated_data['fuel_type']

        existing_vehicle = Vehicle.objects.filter(
            owner=owner,
            category=category,
            make=make,
            model=model,
            year=year,
            price_per_day=price_per_day,
            city=city,
            address=address,
            location=location,
            fuel_type=fuel_type,
        ).first()

        if existing_vehicle:
            raise ValidationError(
                "A vehicle with similar data already exists for the user.")

        # Create the new vehicle
        vehicle = Vehicle.objects.create(**validated_data)

        # Handle features
        for feature_data in features_data:
            feature, created = Feature.objects.get_or_create(
                name=feature_data['name'])
            vehicle.features.add(feature)

        return vehicle


class VehicleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['registration_document', 'insurance_document']


class UpdateVehicleBasicDetailsSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)

    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'price_per_day', 'city',
                  'address', 'location', 'fuel_type', 'availability', 'features']

    def update(self, instance, validated_data):
        features_data = validated_data.pop('features')

        # Update the Vehicle instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update features
        instance.features.clear()
        for feature_data in features_data:
            feature, created = Feature.objects.get_or_create(
                name=feature_data['name'])
            instance.features.add(feature)

        return instance
