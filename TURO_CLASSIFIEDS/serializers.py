from rest_framework import serializers

from TURO.models import Feature, UserProfile, Vehicle, VehicleImages
from TURO.serializers.vehicleSerializers import FeatureSerializer
from TURO_CLASSIFIEDS.models import InterestRequest, Listing




class CreateAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        exclude = ['is_active','ad_status']
        
class UpdateAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        exclude = ['vehicle']

class AddvehicleForSaleSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)
    class Meta:
        model = Vehicle
        exclude = ['price_per_day','availability']
        
class UpdateVehicleDetailsSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)
    class Meta:
        model = Vehicle
        exclude = ['owner','price_per_day','availability']
        
    def update(self, instance, validated_data):
        features_data = validated_data.pop("features")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.features.clear()
        for feature_data in features_data:
            feature, created = Feature.objects.get_or_create(name=feature_data["name"])
            instance.features.add(feature)

        return instance
    
    
class ListingSerializer(serializers.ModelSerializer):
    vehicle = AddvehicleForSaleSerializer()
    thumbnail = serializers.SerializerMethodField()
    class Meta:
        model = Listing
        fields = ['id','thumbnail','listing_date','mileage','price','ad_status','condition','description','vehicle']
        
    def get_thumbnail(self,obj):
        images = VehicleImages.objects.filter(vehicle=obj.vehicle)
        for image in images:
            if image.thumbnail_image:
                return image.thumbnail_image.url
        return None
    
class InterestRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestRequest
        fields = ['buyer', 'listing','request_price']
        
    def validate(self, data):
        listing = data.get('listing')
        request_price = data.get('request_price')

        if listing:
            listing_instance = Listing.objects.get(pk=listing.id)
            original_price = listing_instance.price

            if request_price >= original_price:
                raise serializers.ValidationError("Request price must be less than the original listing price.")

        return data
    
class UpdateInterestRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestRequest
        fields = ['buyer','request_price']
        
    def validate(self, data):
        listing = self.context.get('listing')  
        request_price = data.get('request_price')

        if listing:
            listing_instance = Listing.objects.get(pk=listing.id)
            original_price = listing_instance.price

            if request_price >= original_price:
                raise serializers.ValidationError("Request price must be less than the original listing price.")

        return data
        
class AcceptInterestRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestRequest
        fields = ['status']
        
class SellerProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email') 
    
    class Meta:
        model = UserProfile
        fields = ['email', 'contact_number', 'address']
    
    def validate_contact_number(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("Contact number must be exactly 10 digits.")
        if not value.isdigit():
            raise serializers.ValidationError("Contact number must contain only digits.")
        return value