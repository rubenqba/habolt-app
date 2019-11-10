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
    product_list,
    api_year,
    api_marca,
    api_model,
    api_check,
    api_lead,
    api_lead_end,
    test_pipe
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/<year>', test_pipe, name='test_pipe'),
    path('api/year/<year>', api_year, name='api_year'),
    path('api/brand/<year>/<brand>', api_marca, name='api_marca'),
    path('api/model/<year>/<brand>/<model>', api_model, name='api_model'),
    path('api/check/<year>/<brand>/<model>/<version>/<km>',
         api_check, name='api_check'),
    path('api/lead/create/<name>/<mail>/<phone>/<cp>/<version>',
         api_lead, name='api_lead'),
    path('api/lead/update/<id>/<choose>/<date>/<time>',
         api_lead_end, name='api_lead_end'),
    path('listt/', ListView.as_view(), name='listt'),
    path('list/', product_list, name='list'),
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
    path('vende2/', TemplateView.as_view(template_name='vende.html'), name='vende2'),
    path('vende/', TemplateView.as_view(template_name='vende2.html'), name='vende'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('aviso/', TemplateView.as_view(template_name='aviso.html'), name='aviso')
]
