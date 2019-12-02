from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


CATEGORY_CHOICES = (
    ('A', 'Autos'),
    ('C', 'Classics'),
)

LABEL_CHOICES = (
    ('P', 'Disponible'),
    ('S', 'Apartado'),
    ('D', 'otro')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

TIPO_CHOICES = (
    ('Sedan', 'Sedan'),
    ('SUV', 'SUV'),
    ('Hatch Back', 'Hatch Back'),
    ('Pick-Up', 'Pick-Up'),
    ('Minivan', 'Minivan'),
    ('Coupe', 'Coupe'),
    ('Wagon', 'Wagon'),
    ('4x4', '4x4'),
    ('Convertible', 'Convertible'),
    ('Electrico', 'Electrico'),
)

MARCA_CHOICES = (
    ('Acura', 'Acura'),
    ('Audi', 'Audi'),
    ('BAIC', 'BAIC'),
    ('BMW', 'BMW'),
    ('Buick', 'Buick'),
    ('Cadillac', 'Cadillac'),
    ('Chevrolet', 'Chevrolet'),
    ('Chrysler', 'Chrysler'),
    ('Dodge', 'Dodge'),
    ('Fiat', 'Fiat'),
    ('Ford', 'Ford'),
    ('GMC', 'GMC'),
    ('Honda', 'Honda'),
    ('Hyundai', 'Hyundai'),
    ('Infiniti', 'Infiniti'),
    ('JAC', 'JAC'),
    ('JAC Comerciales', 'JAC Comerciales'),
    ('Jeep', 'Jeep'),
    ('Kia', 'Kia'),
    ('Land Rover', 'Land Rover'),
    ('Lincoln', 'Lincoln'),
    ('Mazda', 'Mazda'),
    ('Mini', 'Mini'),
    ('Mitsubishi', 'Mitsubishi'),
    ('Nissan ', 'Nissan '),
    ('Nissan Comerciales', 'Nissan Comerciales'),
    ('Peugeot', 'Peugeot'),
    ('Peugeot Comerciales', 'Peugeot Comerciales'),
    ('Porsche', 'Porsche'),
    ('Ram Dodge Comerciales', 'Ram Dodge Comerciales'),
    ('Renault', 'Renault'),
    ('Seat', 'Seat'),
    ('Suzuki', 'Suzuki'),
    ('Toyota', 'Toyota'),
    ('Volkswagen', 'Volkswagen'),
    ('Volvo', 'Volvo'),
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField()
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:post", kwargs={
            'slug': self.slug
        })


class Leads(models.Model):
    nombre = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    cp = models.CharField(max_length=100)
    version = models.CharField(max_length=500)
    eleccion = models.CharField(max_length=200)
    status = models.CharField(max_length=100, verbose_name="pipdrive")
    fecha = models.CharField(max_length=100, blank=True, null=True)
    hora = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.IntegerField(blank=False, default=1)
    check = models.IntegerField(blank=False, default=0)
    updated_on = models.DateTimeField(auto_now=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.status


class Kilometrajes(models.Model):
    k_ini = models.IntegerField(blank=False)
    k_fin = models.IntegerField(blank=False)
    ano2019 = models.IntegerField(blank=False)
    ano2018 = models.IntegerField(blank=False)
    ano2017 = models.IntegerField(blank=False)
    ano2016 = models.IntegerField(blank=False)
    ano2015 = models.IntegerField(blank=False)
    ano2014 = models.IntegerField(blank=False)
    ano2013 = models.IntegerField(blank=False)
    ano2012 = models.IntegerField(blank=False)
    ano2011 = models.IntegerField(blank=False)
    ano2010 = models.IntegerField(blank=False)


class Carros(models.Model):
    CONSECUTIVO = models.CharField(max_length=100)
    MARCA = models.CharField(max_length=100)
    NUEVO_USADO = models.CharField(max_length=100)
    ANO_MODELO = models.CharField(max_length=100)
    FORMULA = models.CharField(max_length=100)
    SUBMARCA = models.CharField(max_length=100)
    VERSIÓN = models.CharField(max_length=100)
    PRECIO_VENTA = models.CharField(max_length=100)
    PRECIO_COMPRA = models.CharField(max_length=100)
    TIPO = models.CharField(max_length=100)
    PRECIO_INTERMEDIO = models.CharField(max_length=100)
    PRECIO_AGENCIA_CERTIFICADOS = models.CharField(max_length=100)
    ALGO = models.CharField(max_length=100)
    PRECIO_HABOLT = models.CharField(max_length=100)
    TREINTA_DIAS = models.CharField(max_length=100, blank=True, null=True)
    CONSIGNA = models.CharField(max_length=100)
    PRÉSTAMO = models.CharField(max_length=100)

    def __str__(self):
        return self.VERSIÓN


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField(blank=False)
    discount_price = models.IntegerField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(max_length=200, unique=True)

    year = models.CharField(max_length=100, blank=False)
    marca = models.CharField(choices=MARCA_CHOICES,
                             max_length=100, blank=False)
    km = models.IntegerField(blank=False)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    version = models.CharField(max_length=150, blank=True, null=True)
    codigo = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(choices=TIPO_CHOICES, max_length=100, blank=False)
    color = models.CharField(max_length=100, blank=True, null=True)
    color_int = models.CharField(max_length=100, blank=True, null=True)
    cilindro = models.CharField(max_length=100, blank=True, null=True)
    transmision = models.CharField(max_length=100, blank=True, null=True)
    puertas = models.CharField(max_length=100, blank=True, null=True)
    pasajeros = models.CharField(max_length=100, blank=True, null=True)

    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class ItemImage(models.Model):
    item = models.ForeignKey(
        Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField()


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
