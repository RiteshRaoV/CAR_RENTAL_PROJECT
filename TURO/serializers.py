from dataclasses import fields
from rest_framework import serializers
from .models import Vehicle,Feature,Reservation,Review
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()




class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name']
        
        
class UpdateVehicleDetailSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)

    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'price_per_day', 'location', 'availability', 'features']

    def update(self, instance, validated_data):
        features_data = validated_data.pop('features', [])

        # Update vehicle fields
        instance.make = validated_data.get('make', instance.make)
        instance.model = validated_data.get('model', instance.model)
        instance.year = validated_data.get('year', instance.year)
        instance.price_per_day = validated_data.get('price_per_day', instance.price_per_day)
        instance.location = validated_data.get('location', instance.location)
        instance.availability = validated_data.get('availability', instance.availability)

        instance.features.clear()

        for feature_data in features_data:
            feature_name = feature_data['name']
            existing_feature, created = Feature.objects.get_or_create(name=feature_name)
            instance.features.add(existing_feature)

        instance.save()
        return instance

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["id","username"]

class VehicleDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    class Meta:
        model = Vehicle
        fields = '__all__'
        depth = 1
    # def get_features(self, obj):
    #     return list(obj.features.values_list('name', flat=True))
    
    # def get_owner(self,obj):
    #     return str(obj.owner.username)
    


class AddVehicleSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)  
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'price_per_day', 'location', 'availability', 'owner', 'features']

    def create(self, validated_data):
        features_data = validated_data.pop('features', [])  
        vehicle = Vehicle.objects.create(**validated_data)

        for feature_data in features_data:
            feature_name = feature_data['name']
            existing_feature, created = Feature.objects.get_or_create(name=feature_name)
            vehicle.features.add(existing_feature)

        return vehicle


        