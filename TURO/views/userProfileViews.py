from TURO.models import Reservation, UserProfile
from TURO.serializers.userProfileSerializers import (
    UserProfileDetailSerializer,
    UserProfileSerializer,
)
from rest_framework import generics
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema


class GetUserProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_object(self):
        user_id = self.kwargs.get("user_id")

        try:
            return UserProfile.objects.get(user=user_id)
        except UserProfile.DoesNotExist:
            raise NotFound("User-Profile does not exist")
        
    def perform_destroy(self, instance):
        user = instance.user
        
        if Reservation.objects.filter(user=user, status__in=['pending', 'confirmed']).exists():
            raise PermissionDenied("User cannot be deleted as they have pending or confirmed reservations.")

        instance.delete()

    @swagger_auto_schema(tags=["User-Profile"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["User-Profile"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(tags=["User-Profile"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["User-Profile"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CreateUserProfile(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(tags=["User-Profile"])
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
