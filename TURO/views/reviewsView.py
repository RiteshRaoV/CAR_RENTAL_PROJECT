from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound

from TURO.models import Review
from TURO.serializers.reviewsSerializers import (
    ReviewDetailsSerializer,
    ReviewSerializer,
)


class ReviewsView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @swagger_auto_schema(tags=["Reviews"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Reviews"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ReviewsUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewDetailsSerializer

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        vehicle_id = self.kwargs.get("vehicle_id")

        try:
            return Review.objects.get(user=user_id, vehicle=vehicle_id)
        except Review.DoesNotExist:
            raise NotFound("Review with the specified user and vehicle does not exist.")

    @swagger_auto_schema(tags=["Reviews"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Reviews"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Reviews"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Reviews"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
