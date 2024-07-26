from rest_framework import serializers

from TURO.models import RentListing

class CreateRentListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentListing
        fields = '__all__'
        
class UpdateDeleteRentListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentListing
        exclude = ['vehicle','id']