from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from rest_framework import generics
from rest_framework import filters

from pipedrive.client import Client

from .serializers import CarsSerializer
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile, Carros, Kilometrajes, Leads, Post
from .filters import ItemFilterSet

import random
import string
import stripe
import requests
import json
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class SearchCarsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Item.objects.all()
    serializer_class = CarsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['slug', 'title', 'marca']


class ListCarsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Item.objects.all()
    serializer_class = CarsSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ItemFilterSet


def test_mail(request):
    body = render_to_string(
        'mail/valoracion-mail-habolt.html', {},
    )

    email_message = EmailMessage(
        subject='Mensaje de usuario',
        body=body,
        from_email='support@habolt.mx',
        to=['jj.cabreraarrieta@gmail.com'],
    )
    email_message.content_subtype = 'html'
    email_message.send()
    return JsonResponse({'ok': 'ok'})


def api_newsletter(request, mail):
    token = "b3658f16e23ecc58e6ca38d5fd0009b29b3a7217"
    url = "https://api.pipedrive.com/v1/deals?api_token={}".format(token)
    body = {
        "title": "Newsletter sub : {}".format(mail),
        "stage_id": "8"
    }
    response = requests.post(url, data=body).text
    resj = json.loads(response)

    return JsonResponse(resj['data'], safe=False)


def api_buscamos(request, name, mail, phone, version):
    version = version.replace('|', '/')
    # crear person
    token = "b3658f16e23ecc58e6ca38d5fd0009b29b3a7217"
    url = "https://api.pipedrive.com/v1/persons?api_token={}".format(token)
    body = {
        "name": name,
        "email": mail,
        "phone": phone
    }
    response = requests.post(url, data=body).text
    resj = json.loads(response)
    print(resj['data']['id'])

    # crear deal
    print(version)
    lista = version.split('--')
    print(lista)
    token = "b3658f16e23ecc58e6ca38d5fd0009b29b3a7217"
    url = "https://api.pipedrive.com/v1/deals?api_token={}".format(token)
    body = {
        "title": "Buscar Auto New Habol",
        "stage_id": "2",
        "50bf61363c6260dd0adbb42610ad21174b45d6ea": lista[1],
        "399ed8723c5a919de01c51ce4fd50eae14891d9d": lista[2],
        "1c4a744c38218968766102d798b3f9c40d7ddea9": lista[0],
        "b2541bc70a0ced28452448f312a84ace5282234e": lista[3],
        "cc3795bd66ed72913f5571a6f67ca567d345d24d": "",
        "person_id": resj['data']['id']
    }
    deal = requests.post(url, data=body).text
    res = json.loads(deal)
    print(res['data']['id'])
    new = Leads.objects.create(
        nombre=name, mail=mail, tel=phone, cp="", version=version, eleccion="", status=res['data']['id'], tipo=3
    )

    return JsonResponse({'id': new.id}, safe=False)


def api_compra(request, name, mail, phone, choose, date, time, car, precio):
    date = date.replace('|', '/')
    # crear person
    token = "b3658f16e23ecc58e6ca38d5fd0009b29b3a7217"
    url = "https://api.pipedrive.com/v1/persons?api_token={}".format(token)
    body = {
        "name": name,
        "email": mail,
        "phone": phone
    }
    response = requests.post(url, data=body).text
    resj = json.loads(response)
    print(resj['data']['id'])

    # crear deal
    token = "b3658f16e23ecc58e6ca38d5fd0009b29b3a7217"
    url = "https://api.pipedrive.com/v1/deals?api_token={}".format(token)
    body = {
        "title": "New Habol Compra: {} {}".format(car, precio),
        "stage_id": "2",
        "cc3795bd66ed72913f5571a6f67ca567d345d24d": choose,
        "52d3869a66465bc7f1f8ecc90ba4a6572cc40a7e": date,
        "b0191c0ba8a4d2d6c5c067bd72fda9ce0db68730": time,
        "person_id": resj['data']['id']
    }
    deal = requests.post(url, data=body).text
    res = json.loads(deal)
    print('compra')
    new = Leads.objects.create(
        nombre=name, mail=mail, tel=phone,
        cp="", version=car, eleccion=choose, status=res['data']['id'],
        fecha=date, hora=time, tipo=2
    )

    data = {
        'name': name,
        'mail': mail,
        'phone': phone,
        'date': date,
        'time': time,
        'car': car
    }

    body = render_to_string(
        'mail/agenda-mail-habolt.html', data,
    )

    email_message = EmailMessage(
        subject='Habolt Compra tu Auto',
        body=body,
        from_email='support@habolt.mx',
        to=[mail],
    )
    email_message.content_subtype = 'html'
    email_message.send()

    return JsonResponse({'id': 'ok'}, safe=False)


def api_lead(request, name, mail, phone, cp, version):
    version = version.replace('|', '/')
    # crear person
    token = "b3658f16e23ecc58e6ca38d5fd0009b29b3a7217"
    url = "https://api.pipedrive.com/v1/persons?api_token={}".format(token)
    body = {
        "name": name,
        "email": mail,
        "phone": phone
    }
    response = requests.post(url, data=body).text
    resj = json.loads(response)
    print(resj['data']['id'])

    # crear deal
    print(version)
    lista = version.split('--')
    print(lista)
    token = "b3658f16e23ecc58e6ca38d5fd0009b29b3a7217"
    url = "https://api.pipedrive.com/v1/deals?api_token={}".format(token)
    body = {
        "title": "New Habol Datos Vende",
        "50bf61363c6260dd0adbb42610ad21174b45d6ea": lista[1],
        "399ed8723c5a919de01c51ce4fd50eae14891d9d": lista[2],
        "1c4a744c38218968766102d798b3f9c40d7ddea9": lista[0],
        "b2541bc70a0ced28452448f312a84ace5282234e": lista[3],
        "5aa010b5d0db9a00cffd8cc3d9527f16ca6f25bf": lista[4],
        "cc3795bd66ed72913f5571a6f67ca567d345d24d": "",
        "1ea830209c4978cdc9685df905a7cdabf44f4475": cp,
        "person_id": resj['data']['id']
    }
    deal = requests.post(url, data=body).text
    res = json.loads(deal)
    print(res['data']['id'])
    new = Leads.objects.create(
        nombre=name, mail=mail, tel=phone, cp=cp, version=version, eleccion="", status=res['data']['id']
    )

    return JsonResponse({'id': new.id}, safe=False)


def api_lead_end(request, id, choose, date, time):
    date = date.replace('|', '/')
    activity_type = 10
    key_string = "inspeccin_mec_est"
    print(date)
    lead = Leads.objects.filter(id=id).update(
        eleccion=choose, fecha=date, hora=time
    )
    le = Leads.objects.get(id=id)
    print(le.status)
    token = "b3658f16e23ecc58e6ca38d5fd0009b29b3a7217"
    url = "https://api.pipedrive.com/v1/deals/{}?api_token={}".format(
        le.status, token)
    body = {
        "cc3795bd66ed72913f5571a6f67ca567d345d24d": choose,
        "52d3869a66465bc7f1f8ecc90ba4a6572cc40a7e": date,
        "b0191c0ba8a4d2d6c5c067bd72fda9ce0db68730": time
    }
    deal = requests.put(url, data=body).text
    print(deal)
    lista = le.version.split('--')
    data = {
        'name': le.nombre,
        'mail': le.mail,
        'model': '{} {}'.format(lista[2], lista[3]),
        'brand': lista[1],
        'choose': choose
    }

    body = render_to_string(
        'mail/valoracion-mail-habolt.html', data,
    )

    email_message = EmailMessage(
        subject='Habolt Vende tu Auto',
        body=body,
        from_email='support@habolt.mx',
        to=[le.mail],
    )
    email_message.content_subtype = 'html'
    email_message.send()

    return JsonResponse(lead, safe=False)


def test_pipe(request):
    return JsonResponse({'api': 'ok'}, safe=False)


def api_year(request, year):
    vals = Carros.objects.filter(
        ANO_MODELO=year).distinct('MARCA').values_list('MARCA', flat=True)
    #data = serializers.serialize('json', brands)
    # url = "https://quoting.habolt.mx/quoting/get/year/{}".format(year)
    # res = requests.post(url, verify=False).text
    print(vals)
    return JsonResponse(list(vals), safe=False)


def api_marca(request, year, brand):
    vals = Carros.objects.filter(
        ANO_MODELO=year, MARCA=brand).distinct('SUBMARCA').values_list('SUBMARCA', flat=True)
    # url = "https://quoting.habolt.mx/quoting/get/brand/{}?year={}".format(
    #     brand, year)
    # res = requests.post(url, verify=False).text
    # print(res)
    return JsonResponse(list(vals), safe=False)


def api_model(request, year, brand, model):
    vals = Carros.objects.filter(
        ANO_MODELO=year, MARCA=brand, SUBMARCA=model).distinct('VERSIÓN').values_list('VERSIÓN', flat=True)
    # url = "https://quoting.habolt.mx/quoting/get/model/{}?year={}&brand={}&model={}".format(
    #     model, year, brand, model)
    # res = requests.post(url, verify=False).text
    # print(res)
    return JsonResponse(list(vals), safe=False)


def api_check(request, year, brand, model, version, km):
    version = version.replace('|', '/')
    print(version)
    carro = Carros.objects.filter(
        ANO_MODELO=year, MARCA=brand, SUBMARCA=model, VERSIÓN=version).values('PRECIO_HABOLT', 'TREINTA_DIAS', 'CONSIGNA', 'PRÉSTAMO', 'id').first()
    # result = serializers.serialize('json', carro)
    kms = converter(km)
    key = 'ano{}'.format(year)

    multi = Kilometrajes.objects.filter(
        k_ini__lte=kms, k_fin__gte=kms).extra(select={'value': key}).values('value')

    variable = multi[0]['value'] * 1000
    if carro:
        precio = converter(carro['PRECIO_HABOLT'])
        treinta = converter(carro['TREINTA_DIAS'])
        consigna = converter(carro['CONSIGNA'])
        prestamo = converter(carro['PRÉSTAMO'])

        if precio:
            pp = format((precio + variable), ',')
        else:
            pp = 0

        if treinta:
            pt = format((treinta + variable), ',')
        else:
            pt = 0

        if consigna:
            pc = format((consigna + variable), ',')
        else:
            pc = 0

        if prestamo:
            ppr = format((prestamo + variable), ',')
        else:
            ppr = 0

        data = {
            'precio': pp,
            'treinta': pt,
            'consigna': pc,
            'prestamo': ppr,
            'data': carro
        }
    else:
        data = {
            'precio': 0,
            'treinta': 0,
            'consigna': 0,
            'prestamo': 0,
            'data': carro
        }

    return JsonResponse(data, safe=False)


def converter(cambio):
    try:
        if cambio:
            return int(cambio.replace(',', ''))
    finally:
        a = ''

    return 0


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


class ListView(ListView):
    model = Item
    paginate_by = 10
    template_name = "list.html"


def product_list(request):
    # filter = ItemFilter(request.GET, queryset=Item.objects.all())
    # print(filter)
    return render(request, 'listt.html', {'filter': ''})


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['relacionados'] = Item.objects.all()
        return context


class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
