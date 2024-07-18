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
         views.UpdateVehicleDetails.as_view()),
    path('all-features/',views.FeatureView.as_view()),
    path('vehicle-feature-delete/<int:vehicle_id>/features/<int:feature_id>/', views.RemoveVehicleFeatureView.as_view(), name='remove-vehicle-feature'),
    path('delete-vehicle/<int:vehicle_id>/',views.DeleteVehicleView.as_view())


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
