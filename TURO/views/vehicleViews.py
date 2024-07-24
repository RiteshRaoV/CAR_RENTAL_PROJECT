from TURO import serializers
from TURO.models import UserProfile, Vehicle, VehicleImages
from TURO.serializers.vehicleSerializers import (
    UploadVehicleImagesSerializer,
    VehicleBasicDetailsSerializer,
    VehicleDetails,
    VehicleDocumentSerializer,
    UpdateVehicleBasicDetailsSerializer,
)
from django.db.models import Q
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema

from TURO_CLASSIFIEDS.models import Listing


class AddVehicleBasicDetails(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleBasicDetailsSerializer
    
    def perform_create(self, serializer):
        user = serializer.validated_data['owner']
        try:
            UserProfile.objects.get(user=user)
            serializer.save()
        except UserProfile.DoesNotExist:
            raise PermissionDenied("Create your profile to proceed.")
            

    @swagger_auto_schema(tags=["Vehicle"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GetVehicleDetails(generics.RetrieveAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDetails
    lookup_field = "pk"

    @swagger_auto_schema(tags=["Vehicle"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UpdateVehicleDetails(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = UpdateVehicleBasicDetailsSerializer

    @swagger_auto_schema(tags=["Vehicle"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class VehicleDocumentUploadView(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(tags=["Vehicle"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class UploadVehicleImageView(APIView):
    @swagger_auto_schema(tags=["Vehicle"])
    def post(self, request, *args, **kwargs):
        serializer = UploadVehicleImagesSerializer(data=request.data)
        if serializer.is_valid():
            vehicle = serializer.validated_data["vehicle"]
            images = request.FILES.getlist("images")
            thumbnail = request.FILES.get("thumbnail")
            if thumbnail:
                VehicleImages.objects.create(vehicle=vehicle, thumbnail_image=thumbnail)
            for image in images:
                VehicleImages.objects.create(vehicle=vehicle, vehicle_image=image)
            return Response(
                {"message": "Images uploaded successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteVehicleView(APIView):
    @swagger_auto_schema(tags=["Vehicle"])
    def delete(self, request, vehicle_id, *args, **kwargs):
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            reservations = vehicle.reservations.filter(
                Q(status="pending") | Q(status="confirmed")
            )

            if reservations.exists():
                return Response(
                    {"error": "Vehicle has pending reservations"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if Listing.objects.filter(vehicle=vehicle_id,ad_status__in=['For Sale']).exists():
                return Response(
                    {"error": "Vehicle is listed for sale,delete the listing to proceed"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            vehicle.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Vehicle.DoesNotExist:
            return Response(
                {"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND
            )
