from django.views.generic.base import TemplateView
from django.urls import path
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    ListView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    test,
    product_list
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('list/', ListView.as_view(), name='list'),
    path('listt/', product_list),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('productest/<slug>/', test, name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('nosotros/', TemplateView.as_view(template_name='nosotros.html'),
         name='nosotros'),
    path('vende/', TemplateView.as_view(template_name='vende.html'), name='vende'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('aviso/', TemplateView.as_view(template_name='aviso.html'), name='aviso')
]
