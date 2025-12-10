from django.db.models import Q, Count, F
from main_app.models import Profile, Product, Order
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


def get_profiles(search_string=None):
    profiles = Profile.objects.annotate(order_count=Count('order'))

    if search_string is not None:
        profiles = profiles.filter(
            Q(full_name__icontains=search_string) |
            Q(email__icontains=search_string) |
            Q(phone_number__icontains=search_string)
        )

    profiles = profiles.order_by('full_name')

    if not profiles.exists():
        return ""

    result = []
    for p in profiles:
        result.append(
            f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.order_count}"
        )
    return "\n".join(result)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles.exists():
        return ""

    result = []
    for p in profiles:
        result.append(f"Profile: {p.full_name}, orders: {p.order_count}")
    return "\n".join(result)


def get_last_sold_products():
    last_order = Order.objects.order_by('-id').first()

    if last_order is None:
        return ""

    products = last_order.products.order_by('name')

    if not products.exists():
        return ""

    names = ", ".join(p.name for p in products)
    return f"Last sold products: {names}"


def get_top_products():
    products = (
        Product.objects
        .annotate(num_orders=Count('order'))
        .filter(num_orders__gt=0)
        .order_by('-num_orders', 'name')[:5]
    )

    if not products.exists():
        return ""

    lines = ["Top products:"]
    for p in products:
        lines.append(f"{p.name}, sold {p.num_orders} times")
    return "\n".join(lines)


def apply_discounts():
    orders = Order.objects.annotate(num_products=Count('products')).filter(
        num_products__gt=2,
        is_completed=False
    )

    updated = orders.update(total_price=F('total_price') * 0.9)

    return f"Discount applied to {updated} orders."


def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if order is None:
        return ""

    for product in order.products.all():
        product.in_stock = product.in_stock - 1
        if product.in_stock == 0:
            product.is_available = False
        product.save()

    order.is_completed = True
    order.save()

    return "Order has been completed!"