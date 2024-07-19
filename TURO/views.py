from TURO import serializers
from TURO.models import Feature, Reservation, UserProfile, Vehicle, VehicleImages
from TURO.serializers import (ApproveReservationSerializer, FeatureSerializer, ReservationSerializer,
                              UploadVehicleImagesSerializer, UserProfileSerializer, UserReservationSerializer,
                              VehicleBasicDetailsSerializer, VehicleDetails, VehicleDocumentSerializer,
                              UpdateVehicleBasicDetailsSerializer, VehicleReservationSerializer)
from django.db.models import Q
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

# Vehicle Views


class AddVehicleBasicDetails(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleBasicDetailsSerializer

    @swagger_auto_schema(tags=['Vehicle'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class GetVehicleDetails(generics.RetrieveAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDetails
    lookup_field = 'pk'

    @swagger_auto_schema(tags=['Vehicle'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UpdateVehicleDetails(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = UpdateVehicleBasicDetailsSerializer

    @swagger_auto_schema(tags=['Vehicle'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Vehicle'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class VehicleDocumentUploadView(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(tags=['Vehicle'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class UploadVehicleImageView(APIView):
    @swagger_auto_schema(tags=['Vehicle'])
    def post(self, request, *args, **kwargs):
        serializer = UploadVehicleImagesSerializer(data=request.data)
        if serializer.is_valid():
            vehicle = serializer.validated_data['vehicle']
            images = request.FILES.getlist('images')
            thumbnail = request.FILES.get('thumbnail')
            if thumbnail:
                VehicleImages.objects.create(
                    vehicle=vehicle, thumbnail_image=thumbnail)
            for image in images:
                VehicleImages.objects.create(
                    vehicle=vehicle, vehicle_image=image)
            return Response({"message": "Images uploaded successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Feature Views


class FeatureView(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    @swagger_auto_schema(tags=['Feature'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RemoveVehicleFeatureView(APIView):
    @swagger_auto_schema(tags=['Feature'])
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

# Reservation Views


class DeleteVehicleView(APIView):
    @swagger_auto_schema(tags=['Vehicle'])
    def delete(self, request, vehicle_id, *args, **kwargs):
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            reservations = vehicle.reservations.filter(
                Q(status='pending') | Q(status='confirmed'))

            if reservations.exists():
                return Response({"error": "Vehicle has pending reservations"}, status=status.HTTP_400_BAD_REQUEST)

            vehicle.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Vehicle.DoesNotExist:
            return Response({"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)


class CreateReservationView(APIView):
    @swagger_auto_schema(
        tags=['Reservation'],
        request_body=ReservationSerializer,
        responses={201: ReservationSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user']
            try:
                user = UserProfile.objects.get(user=user_id)
            except UserProfile.DoesNotExist:
                return Response({'error': 'UserProfile does not exist for the provided user ID'}, status=status.HTTP_404_NOT_FOUND)
            if user.dl_image and user.aadhar_image:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                missing_docs = []
                if not user.dl_image:
                    missing_docs.append('Driving License')
                if not user.aadhar_image:
                    missing_docs.append('Aadhar Card')

                missing_docs_str = ', '.join(missing_docs)
                return Response({'error': f'Please upload your {missing_docs_str}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelReservationView(APIView):
    @swagger_auto_schema(
        tags=['Reservation'],
        request_body=ApproveReservationSerializer,
        responses={201: ApproveReservationSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = ApproveReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation_id = serializer.validated_data['reservation_id']
            otp = serializer.validated_data['otp']

            try:
                reservation = Reservation.objects.get(id=reservation_id)
                vehicle = reservation.vehicle
                if reservation.otp == otp:
                    reservation.status = 'cancelled'
                    reservation.otp = ' '
                    reservation.total_price = 0
                    reservation.save()
                    vehicle.availability = True
                    vehicle.save()
                    return Response({'status': 'Reservation Cancelled'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except Reservation.DoesNotExist:
                return Response({'error': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApproveReservationView(APIView):
    @swagger_auto_schema(
        tags=['Reservation'],
        request_body=ApproveReservationSerializer,
        responses={201: ApproveReservationSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = ApproveReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation_id = serializer.validated_data['reservation_id']
            otp = serializer.validated_data['otp']

            try:
                reservation = Reservation.objects.get(id=reservation_id)
                if reservation.otp == otp:
                    reservation.status = 'confirmed'
                    reservation.save()
                    return Response({'status': 'Reservation confirmed'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except Reservation.DoesNotExist:
                return Response({'error': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReservationsView(APIView):
    @swagger_auto_schema(tags=['Reservation'])
    def get(self, request, user_id, format=None):
        try:
            reservations = Reservation.objects.filter(user_id=user_id)
            serializer = UserReservationSerializer(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response({"error": "User not found or no reservations"}, status=status.HTTP_404_NOT_FOUND)


class VehicleReservations(APIView):
    @swagger_auto_schema(tags=['Reservation'])
    def get(self, request, vehicle_id, format=None):
        try:
            reservations = Reservation.objects.filter(vehicle_id=vehicle_id)
            serializer = VehicleReservationSerializer(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response({"error": "User not found or no reservations"}, status=status.HTTP_404_NOT_FOUND)


class GetUserProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user'
    
    @swagger_auto_schema(tags=['User-Profile'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['User-Profile'])
    def delete(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['User-Profile'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CreateUserProfile(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(tags=['User-Profile'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    # @swagger_auto_schema(tags=['User-Profile'])
    # def get(self, request, user_id, *args, **kwargs):
    #     try:
    #         userprofile = UserProfile.objects.get(user=user_id)
    #         serializer = UserProfileSerializer(userprofile)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except UserProfile.DoesNotExist:
    #         return Response({'error': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)
    # @swagger_auto_schema(
    #     tags=['User-Profile'],
    #     request_body=UserProfileSerializer,
    #     responses={201: UserProfileSerializer}
    # )
    # def post(self,request,*args, **kwargs):
    #     pass
