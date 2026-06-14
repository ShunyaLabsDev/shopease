from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product
from store.views import get_cart, save_cart
from .models import Order, OrderItem
from .forms import CheckoutForm


def checkout_view(request):
    cart = get_cart(request)
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect("store:cart")

    # Build cart items
    items = []
    subtotal = 0
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(pk=product_id, is_active=True)
            line = product.effective_price * item["qty"]
            subtotal += line
            items.append({"product": product, "qty": item["qty"], "subtotal": line})
        except Product.DoesNotExist:
            pass

    shipping = 0 if subtotal >= 500 else 50  # Free shipping over ₹500
    total = subtotal + shipping

    form = CheckoutForm(user=request.user if request.user.is_authenticated else None)

    if request.method == "POST":
        form = CheckoutForm(
            user=request.user if request.user.is_authenticated else None,
            data=request.POST,
        )
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.subtotal = subtotal
            order.shipping_cost = shipping
            order.total = total
            order.save()

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    product_name=item["product"].name,
                    price=item["product"].effective_price,
                    quantity=item["qty"],
                )

            # Reduce stock
            for item in items:
                p = item["product"]
                p.stock = max(0, p.stock - item["qty"])
                p.save()

            # Store order id in session for payment
            request.session["pending_order_id"] = order.pk
            return redirect("payments:checkout", order_id=order.pk)

    return render(request, "orders/checkout.html", {
        "form": form,
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    })


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    # Clear cart
    save_cart(request, {})
    return render(request, "orders/order_success.html", {"order": order})
