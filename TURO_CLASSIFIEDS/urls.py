from django.urls import path

from .views import AcceptInterestRequest, AddVehicleForSaleView, AllListings, CreateAdView, GetSellerProfile, InterestRequestCreateView, UpdateAdView, UpdateInterestRequestView, UpdateSellingVehicleDetails


urlpatterns = [
    path('add-vehicle/',AddVehicleForSaleView.as_view(),name="add-vehicle-for-sale"),
    path('update-vehicle/<int:vehicle_id>',UpdateSellingVehicleDetails.as_view(),name='update-vehicel'),
    path('create-listing/',CreateAdView.as_view(),name='create-ad'),
    path('update-listing/<int:listing_id>/',UpdateAdView.as_view(),name='update-ad'),
    path('all-listings/',AllListings.as_view()),
    path('create-request/',InterestRequestCreateView.as_view()),
    path('approve-reject-request/request/<int:request_id>/owner/<int:owner_id>',AcceptInterestRequest.as_view()),
    path('update-request/<int:request_id>/',UpdateInterestRequestView.as_view()),
    path('seller-profile/<int:request_id>/',GetSellerProfile.as_view())

]
