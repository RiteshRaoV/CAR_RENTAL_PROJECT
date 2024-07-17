
from django.shortcuts import render

from TURO.serializers import FeatureSerializer, UpdateVehicleDetailSerializer, VehicleDetailSerializer, AddVehicleSerializer
from .models import Feature, Vehicle,Reservation,Review
from django.contrib.auth import get_user_model
from rest_framework import generics,status
from rest_framework.response import Response

User = get_user_model()

# Create your views here.
class Getalldata(generics.ListAPIView):
     queryset = Vehicle.objects.all()
     serializer_class = VehicleDetailSerializer

class GetVehicleById(generics.ListAPIView):
    serializer_class = VehicleDetailSerializer

    def get_queryset(self):
        vehicle_id = self.kwargs['id']  
        queryset = Vehicle.objects.filter(id=vehicle_id)
        return queryset
    
    
class AddNewVehicle(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = AddVehicleSerializer

    def perform_create(self, serializer):
        make = serializer.validated_data['make']
        model = serializer.validated_data['model']
        owner = serializer.validated_data['owner']

        existing_vehicle = Vehicle.objects.filter(make=make, model=model, owner=owner).exists()

        if existing_vehicle:
            return Response({"message": "This vehicle already exists for the same owner."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
    


class UpdateVehicleDetails(generics.UpdateAPIView):
    serializer_class = UpdateVehicleDetailSerializer
    queryset = Vehicle.objects.all()
    lookup_field = 'id' 
    def get_queryset(self):
        vehicle_id = self.kwargs['id']
        queryset = self.queryset.filter(id=vehicle_id)
        return queryset


class GetAllFeatures(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    