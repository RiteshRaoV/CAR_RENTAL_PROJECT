from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound, PermissionDenied,ValidationError

from TURO.models import Feature, UserProfile, Vehicle
from TURO_CLASSIFIEDS.models import InterestRequest, Listing
from TURO_CLASSIFIEDS.serializers import AcceptInterestRequestSerializer, AddvehicleForSaleSerializer, CreateAdSerializer, InterestRequestSerializer, ListingSerializer, SellerProfileSerializer, UpdateAdSerializer, UpdateInterestRequestSerializer, UpdateVehicleDetailsSerializer


class AllListings(generics.ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class CreateAdView(APIView):
    @swagger_auto_schema(request_body=CreateAdSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CreateAdSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            vehicle = validated_data['vehicle']

            try:
                vehicle_instance = Vehicle.objects.get(id=vehicle.id)
            except Vehicle.DoesNotExist:
                return Response(
                    {"message": "Vehicle does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )

            if Listing.objects.filter(vehicle=vehicle_instance).exists():
                return Response(
                    {"message": "Ad for this vehicle already exists!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if vehicle_instance.registration_document and vehicle_instance.insurance_document:
                listing = Listing.objects.create(
                    vehicle=vehicle_instance,
                    mileage=validated_data['mileage'],
                    price=validated_data['price'],
                    condition=validated_data['condition'],
                    description=validated_data['description']
                )
                return Response(
                    {"message": "Ad created successfully.",
                     "listing": ListingSerializer(listing).data},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"message": "Upload your Vehicle documents to proceed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UpdateAdView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = UpdateAdSerializer

    def get_object(self):
        listing_id = self.kwargs.get('listing_id')

        try:
            return Listing.objects.get(pk=listing_id)
        except Listing.DoesNotExist:
            raise NotFound("Listing does not exist for the given id.")

    def perform_destroy(self, instance):
        if instance.ad_status in ['pending']:
            raise PermissionDenied(
                "Listing cannot be deleted as it is under process.")

        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ListingSerializer
        return super().retrieve(request, *args, **kwargs)


class AddVehicleForSaleView(APIView):
    @swagger_auto_schema(request_body=AddvehicleForSaleSerializer)
    def post(self, request, *args, **kwargs):

        serializer = AddvehicleForSaleSerializer(data=request.data)
        if serializer.is_valid():
            features_data = serializer.validated_data.pop("features")

            owner = serializer.validated_data["owner"]
            category = serializer.validated_data["category"]
            make = serializer.validated_data["make"]
            model = serializer.validated_data["model"]
            year = serializer.validated_data["year"]
            engine_capacity = serializer.validated_data["engine_capacity"]
            transmission = serializer.validated_data["transmission"]
            city = serializer.validated_data["city"]
            address = serializer.validated_data["address"]
            location = serializer.validated_data["location"]
            fuel_type = serializer.validated_data["fuel_type"]
            existing_vehicle = Vehicle.objects.filter(
                owner=owner,
                category=category,
                make=make,
                model=model,
                year=year,
                engine_capacity=engine_capacity,
                transmission=transmission,
                city=city,
                address=address,
                location=location,
                fuel_type=fuel_type,
            ).first()

            if existing_vehicle:
                return Response(
                    {
                        "message": "A vehicle with similar data already exists for the user.",
                        "vehicle": AddvehicleForSaleSerializer(existing_vehicle).data
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                new_vehicle = Vehicle.objects.create(
                    owner=owner,
                    category=category,
                    make=make,
                    model=model,
                    year=year,
                    engine_capacity=engine_capacity,
                    transmission=transmission,
                    city=city,
                    address=address,
                    location=location,
                    fuel_type=fuel_type,
                )
                for feature_data in features_data:
                    feature, created = Feature.objects.get_or_create(
                        name=feature_data["name"])
                    new_vehicle.features.add(feature)

                return Response(
                    {"message": "vehicle added successfully!",
                        "vehicle": AddvehicleForSaleSerializer(new_vehicle).data},
                    status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UpdateSellingVehicleDetails(generics.RetrieveUpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = UpdateVehicleDetailsSerializer

    def get_object(self):
        vehicle_id = self.kwargs.get('vehicle_id')

        if not Listing.objects.filter(vehicle__id=vehicle_id).exists():
            raise NotFound("Vehicle does not have an associated listing.")

        try:
            return Vehicle.objects.get(pk=vehicle_id)
        except Vehicle.DoesNotExist:
            raise NotFound("Vehicle does not exist.")

class InterestRequestCreateView(generics.CreateAPIView):
    serializer_class = InterestRequestSerializer
    
    def perform_create(self, serializer):
        listing = serializer.validated_data['listing']
        buyer = serializer.validated_data['buyer']
        
        if InterestRequest.objects.filter(buyer=buyer, listing=listing).exists():
            raise ValidationError("Request for this listing already exists!")
        
        if Listing.objects.filter(id=listing.id, vehicle__owner=buyer).exists():
            raise PermissionDenied("Buyer and seller cannot be the same person.")
        
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"message": "Request sent successfully!"},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AcceptInterestRequest(generics.UpdateAPIView):
    queryset = InterestRequest.objects.all()
    serializer_class = AcceptInterestRequestSerializer
    
    def get_object(self):
        request_id = self.kwargs.get('request_id')
        owner_id = self.kwargs.get('owner_id')
        try:
            interest_request = InterestRequest.objects.get(pk=request_id)
        except InterestRequest.DoesNotExist:
            raise NotFound("Interest request does not exist.")

        if interest_request.listing.vehicle.owner.id != owner_id:
            raise PermissionDenied("You do not have permission to update this request.")

        return interest_request
    
class UpdateInterestRequestView(generics.UpdateAPIView):
    queryset = InterestRequest.objects.all()
    serializer_class = UpdateInterestRequestSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        interest_request = self.get_object()
        listing = interest_request.listing
        context['listing'] = listing
        return context

    def get_object(self):
        request_id = self.kwargs.get('request_id')
        try:
            return InterestRequest.objects.get(pk=request_id)
        except InterestRequest.DoesNotExist:
            raise ValidationError("No request found for the given id")

class GetSellerProfile(APIView):
    def get(self,*args, **kwargs):
        request_id = self.kwargs.get('request_id')
        try:
            request=InterestRequest.objects.get(pk=request_id)
        except InterestRequest.DoesNotExist:
            raise NotFound("Interest request does not exist.")

        if request.status not in ['pending','rejected']:
            seller = request.listing.vehicle.owner
            seller_profile = UserProfile.objects.get(user=seller)
            return Response(SellerProfileSerializer(seller_profile).data,status=status.HTTP_200_OK)
        else:
            return Response({"error":"Your request is not yet accepted by the seller"},status=status.HTTP_401_UNAUTHORIZED)