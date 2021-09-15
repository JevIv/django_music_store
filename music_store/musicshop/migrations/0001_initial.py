# Generated by Django 3.2.7 on 2021-09-15 17:23

import builtins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils.uploading


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Album name')),
                ('songs_list', models.CharField(max_length=1024, verbose_name='Track list')),
                ('release_date', models.DateField(verbose_name='Release date')),
                ('description', models.CharField(default='Description is coming soon', max_length=1024, verbose_name='Description')),
                ('stock', models.IntegerField(default=1, verbose_name='Available in stock')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Price')),
                ('offer_of_the_week', models.BooleanField(default=False, verbose_name='Offer of the week?')),
                ('slug', models.SlugField()),
                ('image', models.ImageField(upload_to=utils.uploading.upload_function)),
            ],
            options={
                'verbose_name': 'Album',
                'verbose_name_plural': 'Albums',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_products', models.IntegerField(default=0, verbose_name='Total products quantity')),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Total price')),
                ('in_order', models.BooleanField(default=False)),
                ('for_anonymous_user', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active?')),
                ('phone', models.CharField(max_length=20, verbose_name='Telephone number')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name of genre')),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.CreateModel(
            name='MediaType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Type of media')),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Media',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name of musician')),
                ('slug', models.SlugField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
            ],
            options={
                'verbose_name': 'Musician',
                'verbose_name_plural': 'Musicians',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('phone', models.CharField(max_length=20, verbose_name='Telephone number')),
                ('address', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address')),
                ('status', models.CharField(choices=[('new', 'New order'), ('in_progress', 'Order in progress'), ('is_ready', 'Order is ready'), ('completed', 'Customer received order')], default='new', max_length=100, verbose_name='Order status')),
                ('buying_type', models.CharField(choices=[('self', 'Self collection'), ('delivery', 'Delivery')], max_length=100, verbose_name='Order type')),
                ('comment', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Comments about order')),
                ('created_at', models.DateField(auto_now=True, verbose_name='Order placed date')),
                ('order_date', models.DateField(default=django.utils.timezone.now, verbose_name='Date of order receiving')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicshop.cart', verbose_name='Cart')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='musicshop.customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicshop.customer')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to=utils.uploading.upload_function)),
                ('use_in_slider', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Image Gallery',
                'verbose_name_plural': 'Image Gallery',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_orders',
            field=models.ManyToManyField(blank=True, related_name='related_customer', to='musicshop.Order', verbose_name='Customers orders'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Customer'),
        ),
        migrations.AddField(
            model_name='customer',
            name='wishlist',
            field=models.ManyToManyField(blank=True, to='musicshop.Album', verbose_name='Wishlist'),
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveBigIntegerField(verbose_name=builtins.id)),
                ('qty', models.PositiveBigIntegerField(default=1)),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Total price')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicshop.cart', verbose_name='Cart')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicshop.customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Cart product',
                'verbose_name_plural': 'Cart products',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicshop.customer', verbose_name='Customer'),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(blank=True, null=True, related_name='related_cart', to='musicshop.CartProduct', verbose_name='Cart products'),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Artist name/group')),
                ('slug', models.SlugField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicshop.genre')),
                ('members', models.ManyToManyField(related_name='artist', to='musicshop.Member', verbose_name='Band member')),
            ],
            options={
                'verbose_name': 'Artist',
                'verbose_name_plural': 'Artists',
            },
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicshop.artist', verbose_name='Artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicshop.genre'),
        ),
        migrations.AddField(
            model_name='album',
            name='media_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicshop.mediatype', verbose_name='Media'),
        ),
    ]
