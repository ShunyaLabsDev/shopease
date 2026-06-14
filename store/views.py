from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category, Review, Wishlist
from .forms import ReviewForm


# ─── Home ─────────────────────────────────────────────────────────────────────

def home(request):
    featured = Product.objects.filter(is_active=True, is_featured=True)[:8]
    categories = Category.objects.filter(is_active=True, parent=None)
    new_arrivals = Product.objects.filter(is_active=True).order_by("-created_at")[:8]
    on_sale = Product.objects.filter(is_active=True, discount_price__isnull=False)[:8]
    return render(request, "store/home.html", {
        "featured": featured,
        "categories": categories,
        "new_arrivals": new_arrivals,
        "on_sale": on_sale,
    })


# ─── Product List ──────────────────────────────────────────────────────────────

def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True, parent=None)

    # Filters
    category_slug = request.GET.get("category")
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    in_stock = request.GET.get("in_stock", "")

    if category_slug:
        cat = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=cat)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        )

    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    if in_stock:
        products = products.filter(stock__gt=0)

    sort_options = {
        "price_asc": "price",
        "price_desc": "-price",
        "newest": "-created_at",
        "name_asc": "name",
    }
    if sort in sort_options:
        products = products.order_by(sort_options[sort])

    paginator = Paginator(products, 12)
    page = request.GET.get("page", 1)
    products_page = paginator.get_page(page)

    return render(request, "store/product_list.html", {
        "products": products_page,
        "categories": categories,
        "selected_category": category_slug,
        "query": query,
        "sort": sort,
        "min_price": min_price,
        "max_price": max_price,
        "in_stock": in_stock,
        "total_count": paginator.count,
    })


# ─── Product Detail ────────────────────────────────────────────────────────────

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    review_form = ReviewForm()
    user_reviewed = False

    if request.user.is_authenticated:
        user_reviewed = Review.objects.filter(product=product, user=request.user).exists()

    if request.method == "POST" and request.user.is_authenticated and not user_reviewed:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            r = review_form.save(commit=False)
            r.product = product
            r.user = request.user
            r.save()
            messages.success(request, "Review submitted!")
            return redirect("store:product_detail", slug=slug)

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    return render(request, "store/product_detail.html", {
        "product": product,
        "related": related,
        "review_form": review_form,
        "user_reviewed": user_reviewed,
        "in_wishlist": in_wishlist,
    })


# ─── Cart ─────────────────────────────────────────────────────────────────────

def get_cart(request):
    return request.session.get("cart", {})


def save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


def cart_view(request):
    cart = get_cart(request)
    items = []
    total = 0
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(pk=product_id, is_active=True)
            subtotal = product.effective_price * item["qty"]
            total += subtotal
            items.append({"product": product, "qty": item["qty"], "subtotal": subtotal})
        except Product.DoesNotExist:
            pass
    return render(request, "store/cart.html", {"items": items, "total": total})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_cart(request)
    pid = str(product_id)
    qty = int(request.POST.get("qty", 1))

    if pid in cart:
        cart[pid]["qty"] += qty
    else:
        cart[pid] = {"qty": qty}

    if cart[pid]["qty"] > product.stock:
        cart[pid]["qty"] = product.stock

    save_cart(request, cart)
    messages.success(request, f'"{product.name}" added to cart.')
    return redirect(request.META.get("HTTP_REFERER", "store:cart"))


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        save_cart(request, cart)
    return redirect("store:cart")


def update_cart(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    qty = int(request.POST.get("qty", 1))
    if qty > 0 and pid in cart:
        cart[pid]["qty"] = qty
        save_cart(request, cart)
    elif qty == 0:
        del cart[pid]
        save_cart(request, cart)
    return redirect("store:cart")


# ─── Wishlist ─────────────────────────────────────────────────────────────────

@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "store/wishlist.html", {"items": items})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
        messages.info(request, f'"{product.name}" removed from wishlist.')
    else:
        messages.success(request, f'"{product.name}" added to wishlist.')
    return redirect(request.META.get("HTTP_REFERER", "store:wishlist"))


# ─── Search ───────────────────────────────────────────────────────────────────

def search_view(request):
    query = request.GET.get("q", "")
    products = Product.objects.filter(
        is_active=True
    ).filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Product.objects.none()
    return render(request, "store/search_results.html", {"products": products, "query": query})
