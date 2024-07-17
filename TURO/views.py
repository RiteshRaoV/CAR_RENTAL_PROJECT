from rest_framework import generics
from .models import Vehicle, Reservation, Review, Feature, UserProfile, VehicleImages
from .serializers import (
    VehicleSerializer,
    ReservationSerializer,
    ReviewSerializer,
    FeatureSerializer,
    UserProfileSerializer,
    VehicleImagesSerializer,
)


class FeatureListCreate(generics.ListCreateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class UserProfileListCreate(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class VehicleListCreate(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleImagesListCreate(generics.ListCreateAPIView):
    queryset = VehicleImages.objects.all()
    serializer_class = VehicleImagesSerializer


class VehicleImagesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleImages.objects.all()
    serializer_class = VehicleImagesSerializer


class ReservationListCreate(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
