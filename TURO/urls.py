from django.urls import path
from .views import (
    FeatureListCreate,
    FeatureDetail,
    UserProfileListCreate,
    UserProfileDetail,
    VehicleListCreate,
    VehicleDetail,
    VehicleImagesListCreate,
    VehicleImagesDetail,
    ReservationListCreate,
    ReservationDetail,
    ReviewListCreate,
    ReviewDetail,
)

urlpatterns = [
    path("features/", FeatureListCreate.as_view(), name="feature-list-create"),
    path("features/<int:pk>/", FeatureDetail.as_view(), name="feature-detail"),
    path(
        "user-profiles/",
        UserProfileListCreate.as_view(),
        name="userprofile-list-create",
    ),
    path(
        "user-profiles/<int:pk>/",
        UserProfileDetail.as_view(),
        name="userprofile-detail",
    ),
    path("vehicles/", VehicleListCreate.as_view(), name="vehicle-list-create"),
    path("vehicles/<int:pk>/", VehicleDetail.as_view(), name="vehicle-detail"),
    path(
        "vehicle-images/",
        VehicleImagesListCreate.as_view(),
        name="vehicleimages-list-create",
    ),
    path(
        "vehicle-images/<int:pk>/",
        VehicleImagesDetail.as_view(),
        name="vehicleimages-detail",
    ),
    path(
        "reservations/", ReservationListCreate.as_view(), name="reservation-list-create"
    ),
    path(
        "reservations/<int:pk>/", ReservationDetail.as_view(), name="reservation-detail"
    ),
    path("reviews/", ReviewListCreate.as_view(), name="review-list-create"),
    path("reviews/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
]
