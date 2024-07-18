from TURO.models import Feature, Vehicle
from TURO.serializers import  FeatureSerializer, VehicleBasicDetailsSerializer, VehicleDetails, VehicleDocumentSerializer,UpdateVehicleBasicDetailsSerializer
from django.db.models import Q
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AddVehicleBasicDetails(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleBasicDetailsSerializer
    
class GetVehicleDetails(generics.RetrieveAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDetails
    lookup_field = 'pk'

class UpdateVehicleDetails(generics.UpdateAPIView):
    queryset= Vehicle.objects.all()
    serializer_class = UpdateVehicleBasicDetailsSerializer
    
class VehicleDocumentUploadView(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDocumentSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_object(self):
        return Vehicle.objects.get(pk=self.kwargs['pk'])
    
class FeatureView(generics.ListAPIView):
    queryset=Feature.objects.all()
    serializer_class = FeatureSerializer
    
class RemoveVehicleFeatureView(APIView):
    def delete(self, request, vehicle_id, feature_id, *args, **kwargs):
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            feature = Feature.objects.get(id=feature_id)
            vehicle.features.remove(feature)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Vehicle.DoesNotExist:
            return Response({"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)
        except Feature.DoesNotExist:
            return Response({"error": "Feature not found"}, status=status.HTTP_404_NOT_FOUND)
        
class DeleteVehicleView(APIView):
    def delete(self, request, vehicle_id, *args, **kwargs):
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            reservations = vehicle.reservations.filter(Q(status='pending') | Q(status='confirmed'))

            if reservations.exists():
                return Response({"error": "Vehicle has pending reservations"}, status=status.HTTP_400_BAD_REQUEST)
            
            vehicle.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Vehicle.DoesNotExist:
            return Response({"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)