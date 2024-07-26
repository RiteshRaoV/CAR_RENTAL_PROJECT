from genericpath import exists
from rest_framework import generics

from TURO.models import RentListing, Vehicle
from TURO.serializers.rentListingSerializers import CreateRentListingSerializer, UpdateDeleteRentListingSerializer
from rest_framework.exceptions import NotFound, ValidationError,PermissionDenied
from rest_framework import status


class CreateRentListingView(generics.CreateAPIView):
    queryset = RentListing.objects.all()
    serializer_class = CreateRentListingSerializer

    def perform_create(self, serializer):
        vehicle_id = self.request.data.get('vehicle')

        try:
            vehicle_instance = Vehicle.objects.get(pk=vehicle_id)
        except Vehicle.DoesNotExist:
            raise ValidationError(
                {"vehicle": "Vehicle with the provided ID does not exist."})

        if not vehicle_instance.insurance_document or not vehicle_instance.registration_document:
            raise ValidationError(
                {"vehicle": "Vehicle documents are not complete."})

        if RentListing.objects.filter(vehicle=vehicle_instance).exists():
            raise ValidationError(
                {"vehicle": "An ad for this vehicle already exists."})

        serializer.save(vehicle=vehicle_instance)


class UpdateRentListingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RentListing.objects.all()
    serializer_class = UpdateDeleteRentListingSerializer

    def get_object(self, *args, **kwargs):
        rentlisting_id = self.kwargs.get('id')

        try:
            return RentListing.objects.get(pk=rentlisting_id)
        except RentListing.DoesNotExist:
            raise ValidationError(
                {"RentListing": "RentListing with the provided ID does not exist."})

    def perform_update(self, serializer):
        rentlisting = self.get_object()
        validated_data = serializer.validated_data
        validated_data.pop('vehicle', None)
        for attr, value in validated_data.items():
            setattr(rentlisting, attr, value)
        rentlisting.save()

    def perform_destroy(self, instance):
        listings = instance.vehicle.rent_listings.get()
        if listings.reservations.filter(status__in = ['pending','confirmed']).exists():
            raise PermissionDenied(
                "Listing cannot be deleted as it has pending reservations.")
        instance.delete()