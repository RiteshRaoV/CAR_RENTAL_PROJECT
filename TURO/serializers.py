from TURO.models import Feature, Vehicle
from rest_framework import serializers

from rest_framework.exceptions import ValidationError
from .models import Reservation, VehicleImages

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


import random
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['vehicle', 'user', 'start_date', 'end_date']

    def create(self, validated_data):
        vehicle = validated_data['vehicle']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        
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
            user=validated_data['user'],
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status='pending',
            otp=otp
        )

        # Set vehicle availability to false
        vehicle.availability = False
        vehicle.save()

        return reservation
    
class ApproveReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    otp = serializers.CharField(max_length=6)
    

class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImages
        fields = ['vehicle_image']

class UploadVehicleImagesSerializer(serializers.Serializer):
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())
    images = serializers.ListField(
        child=serializers.ImageField(max_length=100000),
        write_only=True
    )


class UserReservationSerializer(serializers.ModelSerializer):
    vehicle_make = serializers.CharField(source='vehicle.make')
    vehicle_model = serializers.CharField(source='vehicle.model')
    vehicle_id = serializers.IntegerField(source = 'vehicle.id')
    class Meta:
        model = Reservation
        fields = ['id','vehicle_id' ,'vehicle_make', 'vehicle_model', 'user', 'start_date', 'end_date','status']

class VehicleReservationSerializer(serializers.ModelSerializer):
    vehicle_make = serializers.CharField(source='vehicle.make')
    vehicle_model = serializers.CharField(source='vehicle.model')
    vehicle_id = serializers.IntegerField(source = 'vehicle.id')
    reservation_id = serializers.IntegerField(source = 'id')
    class Meta:
        model = Reservation
        fields = ['reservation_id','vehicle_id' ,'vehicle_make', 'vehicle_model', 'user', 'start_date', 'end_date','total_price','status']
