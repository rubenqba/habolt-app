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

from rest_framework import generics
from rest_framework import filters

from pipedrive.client import Client

from .serializers import CarsSerializer
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile, Carros, Kilometrajes, Leads
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


def api_cars(request):
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


def api_compra(request, name, mail, phone, choose, date, time, precio, car):
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
    print(res['data']['id'])

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
    return JsonResponse(lead, safe=False)


def test_pipe(request):
    return JsonResponse({'api': 'ok'}, safe=False)


def api_year(request, year):
    url = "https://quoting.habolt.mx/quoting/get/year/{}".format(year)
    res = requests.post(url, verify=False).text
    print(res)
    return JsonResponse(res, safe=False)


def api_marca(request, year, brand):
    url = "https://quoting.habolt.mx/quoting/get/brand/{}?year={}".format(
        brand, year)
    res = requests.post(url, verify=False).text
    print(res)
    return JsonResponse(res, safe=False)


def api_model(request, year, brand, model):
    url = "https://quoting.habolt.mx/quoting/get/model/{}?year={}&brand={}&model={}".format(
        model, year, brand, model)
    res = requests.post(url, verify=False).text
    print(res)
    return JsonResponse(res, safe=False)


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
        print(variable)
        print(precio)
        print(precio + variable)
        data = {
            'precio': format((precio + variable), ','),
            'treinta': format((treinta + variable), ','),
            'consigna': format((consigna + variable), ','),
            'prestamo': format((prestamo + variable), ','),
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


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")


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


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['relacionados'] = Item.objects.all()
        return context


def test(request, slug):
    print(slug)
    context = {}
    context['object'] = get_object_or_404(Item, slug=slug)
    context['relacionados'] = Item.objects.all()
    return render(request, 'product.html', context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")
