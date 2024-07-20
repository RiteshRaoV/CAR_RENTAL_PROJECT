from TURO.models import Reservation, UserProfile
from TURO.serializers.reservationSerializers import (
    ApproveReservationSerializer,
    ReservationSerializer,
    UserReservationSerializer,
    VehicleReservationSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class CreateReservationView(APIView):
    @swagger_auto_schema(
        tags=["Reservation"],
        request_body=ReservationSerializer,
        responses={201: ReservationSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data["user"]
            try:
                user = UserProfile.objects.get(user=user_id)
            except UserProfile.DoesNotExist:
                return Response(
                    {"error": "UserProfile does not exist for the provided user ID"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if user.dl_image and user.aadhar_image:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                missing_docs = []
                if not user.dl_image:
                    missing_docs.append("Driving License")
                if not user.aadhar_image:
                    missing_docs.append("Aadhar Card")

                missing_docs_str = ", ".join(missing_docs)
                return Response(
                    {"error": f"Please upload your {missing_docs_str}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelReservationView(APIView):
    @swagger_auto_schema(
        tags=["Reservation"],
        request_body=ApproveReservationSerializer,
        responses={201: ApproveReservationSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = ApproveReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation_id = serializer.validated_data["reservation_id"]
            otp = serializer.validated_data["otp"]

            try:
                reservation = Reservation.objects.get(id=reservation_id)
                vehicle = reservation.vehicle
                if reservation.otp == otp:
                    reservation.status = "cancelled"
                    reservation.otp = " "
                    reservation.total_price = 0
                    reservation.save()
                    vehicle.availability = True
                    vehicle.save()
                    return Response(
                        {"status": "Reservation Cancelled"}, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
                    )
            except Reservation.DoesNotExist:
                return Response(
                    {"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApproveReservationView(APIView):
    @swagger_auto_schema(
        tags=["Reservation"],
        request_body=ApproveReservationSerializer,
        responses={201: ApproveReservationSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = ApproveReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation_id = serializer.validated_data["reservation_id"]
            otp = serializer.validated_data["otp"]

            try:
                reservation = Reservation.objects.get(id=reservation_id)
                if reservation.otp == otp:
                    reservation.status = "confirmed"
                    reservation.save()
                    return Response(
                        {"status": "Reservation confirmed"}, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
                    )
            except Reservation.DoesNotExist:
                return Response(
                    {"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReservationsView(APIView):
    @swagger_auto_schema(tags=["Reservation"])
    def get(self, request, user_id, format=None):
        try:
            reservations = Reservation.objects.filter(user_id=user_id)
            serializer = UserReservationSerializer(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response(
                {"error": "User not found or no reservations"},
                status=status.HTTP_404_NOT_FOUND,
            )


class VehicleReservations(APIView):
    @swagger_auto_schema(tags=["Reservation"])
    def get(self, request, vehicle_id, format=None):
        try:
            reservations = Reservation.objects.filter(vehicle_id=vehicle_id)
            serializer = VehicleReservationSerializer(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response(
                {"error": "User not found or no reservations"},
                status=status.HTTP_404_NOT_FOUND,
            )
