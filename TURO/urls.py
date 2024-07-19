from django.urls import path
from MY_SITE import settings
from TURO import views
from django.conf.urls.static import static

urlpatterns = [
    path('vehicle-details/', views.AddVehicleBasicDetails.as_view(),
         name="add-basic-vehicle-details"),
    path('vehicle-details/<int:pk>/', views.GetVehicleDetails.as_view(),
         name="get-vehicle-details-byID"),
    path('vehicles/<int:pk>/upload-documents/',
         views.VehicleDocumentUploadView.as_view(), name='vehicle-upload-documents'),
    path('update-vehicle-details/<int:pk>/',
         views.UpdateVehicleDetails.as_view(),name='update-vehicle-details'),
    path('upload-vehicle-image/',
         views.UploadVehicleImageView.as_view(),name='upload-vehicle-details'),
    path('all-features/', views.FeatureView.as_view()),
    path('vehicle-feature-delete/<int:vehicle_id>/features/<int:feature_id>/',
         views.RemoveVehicleFeatureView.as_view(), name='remove-vehicle-feature'),
    path('delete-vehicle/<int:vehicle_id>/',
         views.DeleteVehicleView.as_view(),name='delete-vehicle'),
    path('book-reservations/', views.CreateReservationView.as_view(),
         name='book-reservation'),
    path('approve-reservation/', views.ApproveReservationView.as_view(),name='approve-reservation'),
    path('cancel-reservation/', views.CancelReservationView.as_view(),name='cancel-reservation'),
    path('user-reservations/<int:user_id>/',
         views.UserReservationsView.as_view(),name='user-reservations'),
    path('vehicle-reservations/<int:vehicle_id>/',
         views.VehicleReservations.as_view(),name='vehicle-reservations'),
    path('user-profile/<int:user>/',
         views.GetUserProfile.as_view(), name='user-profile'),
    path('create-user-profile/', views.CreateUserProfile.as_view(),
         name='create-user-profile'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
