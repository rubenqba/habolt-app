from import_export import resources
from django.contrib import admin

from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile, ItemImage, Kilometrajes, Carros, Leads, Post
from import_export.admin import ImportExportModelAdmin


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class CarrosResource(resources.ModelResource):

    class Meta:
        model = Carros


class KilometrajesResource(resources.ModelResource):

    class Meta:
        model = Kilometrajes


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


class LeadsAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'version',
        'eleccion',
        'status',
        'tipo',
        'fecha',
        'hora',
        'check'
    ]
    search_fields = ['nombre', 'version', 'status']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 10


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price',
        'slug',
        'year',
        'marca',
        'modelo',
        'version',
        'image'
    ]
    search_fields = ['title', 'slug', 'price']
    inlines = [ItemImageInline, ]


class CarrosAdmin(ImportExportModelAdmin):
    resource_class = CarrosResource


class KilometrajesAdmin(ImportExportModelAdmin):
    resource_class = KilometrajesResource


admin.site.register(Kilometrajes, KilometrajesAdmin)
admin.site.register(Carros, CarrosAdmin)

admin.site.register(Item, ItemAdmin)

# admin.site.register(Kilometrajes)
# admin.site.register(Carros)

admin.site.register(Post, PostAdmin)
admin.site.register(Leads, LeadsAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
