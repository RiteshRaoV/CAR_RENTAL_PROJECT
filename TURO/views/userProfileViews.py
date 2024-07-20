from TURO.models import UserProfile
from TURO.serializers.userProfileSerializers import UserProfileSerializer
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema


class GetUserProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "user"

    @swagger_auto_schema(tags=["User-Profile"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["User-Profile"])
    def delete(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["User-Profile"])
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
