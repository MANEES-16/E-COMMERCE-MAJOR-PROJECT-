from django.db import migrations
from django.contrib.auth.hashers import make_password
from decimal import Decimal


def seed_initial_data(apps, schema_editor):
    Product = apps.get_model('base', 'Product')
    User = apps.get_model('auth', 'User')

    if Product.objects.exists():
        return

    admin_email = 'admin@example.com'
    admin_defaults = {
        'email': admin_email,
        'first_name': 'Admin',
        'is_staff': True,
        'is_superuser': True,
    }
    admin_user, created = User.objects.get_or_create(
        username=admin_email,
        defaults=admin_defaults,
    )

    password_updated = False
    if created:
        admin_user.password = make_password('admin123')
        password_updated = True
    else:
        updated = False
        if not admin_user.is_staff:
            admin_user.is_staff = True
            updated = True
        if not admin_user.is_superuser:
            admin_user.is_superuser = True
            updated = True
        if updated:
            admin_user.save(update_fields=['is_staff', 'is_superuser'])

    if password_updated:
        admin_user.save(update_fields=['password'])

    sample_products = [
        {
            'name': 'Running Shoes',
            'price': Decimal('79.99'),
            'brand': 'Stride',
            'category': 'Footwear',
            'description': 'Lightweight running shoes ideal for daily workouts.',
            'countInStock': 15,
            'image': '/images/shoe.jpg',
            'rating': Decimal('4.5'),
            'numReviews': 12,
        },
        {
            'name': 'Vivo Y36 Smartphone',
            'price': Decimal('219.00'),
            'brand': 'Vivo',
            'category': 'Electronics',
            'description': '6.58" display, 8GB RAM, and a 5000mAh battery for all-day power.',
            'countInStock': 9,
            'image': '/images/vivo-mobile.jpg',
            'rating': Decimal('4.2'),
            'numReviews': 7,
        },
        {
            'name': 'Classic White T-Shirt',
            'price': Decimal('19.99'),
            'brand': 'Everyday Basics',
            'category': 'Apparel',
            'description': 'Soft cotton tee with a tailored fit for casual wear.',
            'countInStock': 30,
            'image': '/images/white-t-shirt.jpg',
            'rating': Decimal('4.8'),
            'numReviews': 25,
        },
        {
            'name': 'Bluetooth Headphones',
            'price': Decimal('59.99'),
            'brand': 'SoundWave',
            'category': 'Electronics',
            'description': 'Noise-cancelling over-ear headphones with 20-hour battery life.',
            'countInStock': 20,
            'image': 'https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?auto=format&fit=crop&w=600&q=80',
            'rating': Decimal('4.6'),
            'numReviews': 18,
        },
        {
            'name': 'Smart Fitness Watch',
            'price': Decimal('129.99'),
            'brand': 'PulseTrack',
            'category': 'Wearables',
            'description': 'Track workouts, sleep, and heart rate with built-in GPS.',
            'countInStock': 14,
            'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80',
            'rating': Decimal('4.4'),
            'numReviews': 10,
        },
    ]

    for product_data in sample_products:
        Product.objects.create(user=admin_user, **product_data)


def remove_seed_data(apps, schema_editor):
    Product = apps.get_model('base', 'Product')
    User = apps.get_model('auth', 'User')

    names = [
        'Running Shoes',
        'Vivo Y36 Smartphone',
        'Classic White T-Shirt',
        'Bluetooth Headphones',
        'Smart Fitness Watch',
    ]
    Product.objects.filter(name__in=names).delete()

    try:
        admin_user = User.objects.get(username='admin@example.com')
    except User.DoesNotExist:
        return

    if not admin_user.is_superuser and not admin_user.is_staff:
        admin_user.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_initial_data, reverse_code=remove_seed_data),
    ]
