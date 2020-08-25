from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        if quantity < product.stock:
            total += quantity * product.price
            product_count += quantity

            bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
            })
        elif product.stock == 0:
            if item_id in bag_items:
                bag.pop()
        else:
            total += product.stock * product.price
            product_count += product.stock

            bag_items.append({
                'item_id': item_id,
                'quantity': product.stock,
                'product': product,
            })

    grand_total = total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }

    return context
