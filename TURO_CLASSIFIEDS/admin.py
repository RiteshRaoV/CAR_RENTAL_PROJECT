from django.contrib import admin

from TURO_CLASSIFIEDS.models import InterestRequest, Listing

# Register your models here.


class ListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'listing_date',
                    'is_active', 'price', 'ad_status']


class InterestRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'listing','request_price', 'status', 'request_date']


admin.site.register(Listing, ListingAdmin)
admin.site.register(InterestRequest,InterestRequestAdmin)