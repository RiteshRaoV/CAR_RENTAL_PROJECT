from django.urls import path

from TURO import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("available-vehicles/",views.Getalldata.as_view()),
    path("get-vehicle/<int:id>",views.GetVehicleById.as_view()),
    path("add-vehicle/",views.AddNewVehicle.as_view()),
    path("all-features/",views.GetAllFeatures.as_view()),
    path("update-vehicleDetails/<int:id>",views.UpdateVehicleDetails.as_view())
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
