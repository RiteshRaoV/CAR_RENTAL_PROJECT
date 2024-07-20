from django.urls import path
from MY_SITE import settings
from django.conf.urls.static import static
from TURO.views.vehicleViews import (
    AddVehicleBasicDetails,
    DeleteVehicleView,
    GetVehicleDetails,
    UpdateVehicleDetails,
    UploadVehicleImageView,
    VehicleDocumentUploadView,
)
from TURO.views.featureViews import RemoveVehicleFeatureView, FeatureView
from TURO.views.reservationViews import (
    ApproveReservationView,
    CancelReservationView,
    CreateReservationView,
    UserReservationsView,
    VehicleReservations,
)
from TURO.views.userProfileViews import CreateUserProfile, GetUserProfile

urlpatterns = [
    path(
        "vehicle-details/",
        AddVehicleBasicDetails.as_view(),
        name="add-basic-vehicle-details",
    ),
    path(
        "vehicle-details/<int:pk>/",
        GetVehicleDetails.as_view(),
        name="get-vehicle-details-byID",
    ),
    path(
        "vehicles/<int:pk>/upload-documents/",
        VehicleDocumentUploadView.as_view(),
        name="vehicle-upload-documents",
    ),
    path(
        "update-vehicle-details/<int:pk>/",
        UpdateVehicleDetails.as_view(),
        name="update-vehicle-details",
    ),
    path(
        "upload-vehicle-image/",
        UploadVehicleImageView.as_view(),
        name="upload-vehicle-details",
    ),
    path("all-features/", FeatureView.as_view()),
    path(
        "vehicle-feature-delete/<int:vehicle_id>/features/<int:feature_id>/",
        RemoveVehicleFeatureView.as_view(),
        name="remove-vehicle-feature",
    ),
    path(
        "delete-vehicle/<int:vehicle_id>/",
        DeleteVehicleView.as_view(),
        name="delete-vehicle",
    ),
    path(
        "book-reservations/", CreateReservationView.as_view(), name="book-reservation"
    ),
    path(
        "approve-reservation/",
        ApproveReservationView.as_view(),
        name="approve-reservation",
    ),
    path(
        "cancel-reservation/",
        CancelReservationView.as_view(),
        name="cancel-reservation",
    ),
    path(
        "user-reservations/<int:user_id>/",
        UserReservationsView.as_view(),
        name="user-reservations",
    ),
    path(
        "vehicle-reservations/<int:vehicle_id>/",
        VehicleReservations.as_view(),
        name="vehicle-reservations",
    ),
    path("user-profile/<int:user>/", GetUserProfile.as_view(), name="user-profile"),
    path(
        "create-user-profile/", CreateUserProfile.as_view(), name="create-user-profile"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
