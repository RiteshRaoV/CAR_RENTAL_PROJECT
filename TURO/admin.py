from django.contrib import admin
from .models import RentListing, Vehicle, Reservation, Review, Feature, UserProfile, VehicleImages


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'make', 'model', 'year',
                    'owner', 'created_at', 'updated_at')
    search_fields = ('make', 'model', 'owner__username')
    list_filter = ('year', 'created_at')
    autocomplete_fields = ['owner']
    filter_horizontal = ('features',)


class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'rental_listing',
        'user',
        'start_date',
        'end_date',
        'total_price',
        'status',
        'created_at',
        'updated_at',
        'otp'
    )
    search_fields = (
        'rental_listing__vehicle__make',
        'rental_listing__vehicle__model',
        'user__username',
        'status'
    )
    list_filter = (
        'status',
        'start_date',
        'end_date',
        'created_at'
    )


class RentListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing_date', 'price_per_day',
                    'availability', 'city')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'rating', 'comment', 'created_at')
    search_fields = ('user__username', 'vehicle__make',
                     'vehicle__model', 'rating')
    list_filter = ('rating', 'created_at')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'aadhar_image', 'dl_image')
    search_fields = ('user__username',)
    autocomplete_fields = ['user']


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(VehicleImages)
admin.site.register(RentListing, RentListingAdmin)
