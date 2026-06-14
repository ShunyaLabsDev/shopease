import stripe
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def payment_checkout(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if order.payment_status == "paid":
        return redirect("orders:order_success", order_number=order.order_number)

    # Create Stripe PaymentIntent
    intent = stripe.PaymentIntent.create(
        amount=int(order.total * 100),  # paise / cents
        currency="inr",
        metadata={"order_id": order.pk, "order_number": order.order_number},
    )
    order.stripe_payment_intent = intent.id
    order.save()

    return render(request, "payments/checkout.html", {
        "order": order,
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        "client_secret": intent.client_secret,
    })


def payment_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.payment_status = "paid"
    order.status = "processing"
    order.save()
    # Clear cart
    request.session["cart"] = {}
    request.session.modified = True
    return redirect("orders:order_success", order_number=order.order_number)


def payment_cancel(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    messages.warning(request, "Payment was cancelled. Your order is still saved.")
    return redirect("orders:checkout")


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        order_id = intent["metadata"].get("order_id")
        try:
            order = Order.objects.get(pk=order_id)
            order.payment_status = "paid"
            order.status = "processing"
            order.save()
        except Order.DoesNotExist:
            pass

    elif event["type"] == "payment_intent.payment_failed":
        intent = event["data"]["object"]
        order_id = intent["metadata"].get("order_id")
        try:
            order = Order.objects.get(pk=order_id)
            order.payment_status = "failed"
            order.save()
        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)
