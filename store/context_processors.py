def cart_count(request):
    cart = request.session.get("cart", {})
    count = sum(item["qty"] for item in cart.values())
    return {"cart_count": count}


def categories_nav(request):
    from store.models import Category
    cats = Category.objects.filter(is_active=True, parent=None)[:8]
    return {"categories_nav": cats}
