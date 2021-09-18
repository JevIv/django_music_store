from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from utils import upload_function


class MediaType(models.Model):

    name = models.CharField(max_length=100, verbose_name='Type of media')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media'


class Member(models.Model):
    """Musician"""

    name = models.CharField(max_length=255, verbose_name='Name of musician')
    slug = models.SlugField()
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Musician'
        verbose_name_plural = 'Musicians'


class Genre(models.Model):
    """Musical genre"""

    name = models.CharField(max_length=50, verbose_name='Name of genre')
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Artist(models.Model):
    """Artist"""

    name = models.CharField(max_length=255, verbose_name='Artist name/group')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    members = models.ManyToManyField(Member, verbose_name='Band member', related_name='artist')
    slug = models.SlugField()
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return f"{self.name} | {self.genre.name}"

    def get_absolute_url(self):
        return reverse('artist_detail', kwargs={'artist_slug': self.slug})

    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'


class Album(models.Model):
    """Album"""

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='Artist')
    name = models.CharField(max_length=255, verbose_name='Album name')
    media_type = models.ForeignKey(MediaType, on_delete=models.CASCADE, verbose_name='Media')
    songs_list = models.CharField(max_length=1024, verbose_name='Track list')
    release_date = models.DateField(verbose_name='Release date')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.CharField(max_length=1024, verbose_name='Description', default='Description is coming soon')
    stock = models.IntegerField(default=1, verbose_name='Available in stock')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')
    offer_of_the_week = models.BooleanField(default=False, verbose_name='Offer of the week?')
    slug = models.SlugField()
    image = models.ImageField(upload_to=upload_function)

    def __str__(self):
        return f"{self.id} | {self.artist.name} | {self.name}"

    def get_absolute_url(self):
        return reverse('album_detail', kwargs={'artist_slug': self.artist.slug, 'album_slug': self.slug})

    @property
    def ct_model(self):
        return self._meta.model.name

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'


class CartProduct(models.Model):
    """Cart product"""
    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField(id)
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveBigIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total price')

    def __str__(self):
        return f"Product: {self.content_object.name} (for cart)"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_type.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cart product'
        verbose_name_plural = 'Cart products'


class Cart(models.Model):
    """Cart"""

    owner = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    product = models.ManyToManyField(
        CartProduct, blank=True, related_name='related_cart', verbose_name='Cart products')
    total_products = models.IntegerField(default=0, verbose_name='Total products quantity')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total price')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return (self.id)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class Order(models.Model):
    """Customer order"""

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'New order'),
        (STATUS_IN_PROGRESS, 'Order in progress'),
        (STATUS_READY, 'Order is ready'),
        (STATUS_COMPLETED, 'Customer received order')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Self collection'),
        (BUYING_TYPE_DELIVERY, 'Delivery')
    )

    customer = models.ForeignKey('Customer', verbose_name='Customer', related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='First name')
    last_name = models.CharField(max_length=255, verbose_name='Last name')
    phone = models.CharField(max_length=20, verbose_name='Telephone number')
    cart = models.ForeignKey(Cart, verbose_name='Cart', on_delete=models.CASCADE)
    address = models.CharField(max_length=1024, verbose_name='Address', null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Order status', choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(max_length=100, verbose_name='Order type', choices=BUYING_TYPE_CHOICES)
    comment = models.CharField(max_length=1024, verbose_name='Comments about order', null=True, blank=True)
    created_at = models.DateField(verbose_name='Order placed date', auto_now=True)
    order_date = models.DateField(verbose_name='Date of order receiving', default=timezone.now)

    def __str__(self):
        return  str(self.id)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Customer(models.Model):
    """Customer"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Customer', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='Active?')
    customer_orders = models.ManyToManyField(Order, blank=True, verbose_name='Customers orders', related_name='related_customer')
    wishlist = models.ManyToManyField(Album, verbose_name='Wishlist', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Telephone number')
    address = models.TextField(verbose_name='Address', null=True, blank=True)

    def __str__(self):
        return  f"{self.user.username}"

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Notification(models.Model):
    """Notifications"""

    recipient = models.ForeignKey(Customer, on_delete=models.CASCADE)
    text = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.user.username} | id={self.id}"

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'


class ImageGallery(models.Model):
    """Gallery"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=upload_function)
    use_in_slider = models.BooleanField(default=False)

    def __str__(self):
        return f"Images for {self.content_object}"

    def image_url(self):
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="200px">')

    class Meta:
        verbose_name = 'Image Gallery'
        verbose_name_plural = verbose_name

