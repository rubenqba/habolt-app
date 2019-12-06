from django.views.generic.base import TemplateView
from django.urls import path
from .views import (
    ItemDetailView,
    HomeView,
    ListView,
    product_list,
    api_year,
    api_marca,
    api_model,
    api_check,
    api_lead,
    api_lead_end,
    test_pipe,
    api_newsletter,
    ListCarsView,
    SearchCarsView,
    api_compra,
    api_buscamos,
    PostList,
    PostDetail
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('blog/', PostList.as_view(), name='blog'),
    path('post/<slug>/', PostDetail.as_view(), name='post'),
    path('api/health', test_pipe, name='test_pipe'),
    path('api/cars', ListCarsView.as_view(), name='api_cars'),
    path('api/search', SearchCarsView.as_view(), name='api_search'),
    path('api/newsletter/<mail>', api_newsletter, name='api_newsletter'),
    path('api/year/<year>', api_year, name='api_year'),
    path('api/brand/<year>/<brand>', api_marca, name='api_marca'),
    path('api/model/<year>/<brand>/<model>', api_model, name='api_model'),
    path('api/check/<year>/<brand>/<model>/<version>/<km>/<name>/<mail>/<phone>/<cp>/<ver>',
         api_check, name='api_check'),
    path('api/lead/create/<name>/<mail>/<phone>/<cp>/<version>',
         api_lead, name='api_lead'),
    path('api/compra/<name>/<mail>/<phone>/<choose>/<date>/<time>/<car>/<precio>/<ofertas>',
         api_compra, name='api_compra'),
    path('api/lead/update/<id>/<choose>/<date>/<time>',
         api_lead_end, name='api_lead_end'),
    path('api/buscamos/create/<name>/<mail>/<phone>/<version>/<presupuesto>',
         api_buscamos, name='api_buscamos'),
    path('listt/', ListView.as_view(), name='listt'),
    path('list/', product_list, name='list'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('nosotros/', TemplateView.as_view(template_name='nosotros.html'),
         name='nosotros'),
    path('vende2/', TemplateView.as_view(template_name='vende.html'), name='vende2'),
    path('vende/', TemplateView.as_view(template_name='vende2.html'), name='vende'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('aviso/', TemplateView.as_view(template_name='aviso.html'), name='aviso'),
    path('buscamos/', TemplateView.as_view(template_name='buscamos.html'), name='buscamos')
]
