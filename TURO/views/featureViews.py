from TURO.models import Feature, Vehicle
from TURO.serializers import FeatureSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class FeatureView(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    @swagger_auto_schema(tags=["Feature"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RemoveVehicleFeatureView(APIView):
    @swagger_auto_schema(tags=["Feature"])
    def delete(self, request, vehicle_id, feature_id, *args, **kwargs):
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            feature = Feature.objects.get(id=feature_id)
            vehicle.features.remove(feature)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Vehicle.DoesNotExist:
            return Response(
                {"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Feature.DoesNotExist:
            return Response(
                {"error": "Feature not found"}, status=status.HTTP_404_NOT_FOUND
            )
