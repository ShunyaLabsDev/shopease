"""
Management command to seed the database with sample data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from store.models import Category, Product


CATEGORIES = [
    {"name": "Electronics", "slug": "electronics", "description": "Gadgets, phones, laptops and more"},
    {"name": "Clothing", "slug": "clothing", "description": "Men and women fashion"},
    {"name": "Home & Kitchen", "slug": "home-kitchen", "description": "Everything for your home"},
    {"name": "Books", "slug": "books", "description": "Bestsellers and textbooks"},
    {"name": "Sports", "slug": "sports", "description": "Fitness and outdoor gear"},
    {"name": "Beauty", "slug": "beauty", "description": "Skincare and personal care"},
]

PRODUCTS = [
    {"name": "Wireless Bluetooth Headphones", "category": "electronics", "price": 2999, "discount_price": 1999, "stock": 50, "is_featured": True, "description": "Premium wireless headphones with 30-hour battery life, active noise cancellation, and crystal-clear sound. Compatible with all Bluetooth devices.", "short_description": "ANC headphones with 30h battery life"},
    {"name": "Smartphone 5G Pro", "category": "electronics", "price": 29999, "discount_price": 24999, "stock": 30, "is_featured": True, "description": "Latest 5G smartphone with 6.7-inch AMOLED display, 108MP camera, 5000mAh battery, and 8GB RAM.", "short_description": "108MP camera, 5G, 8GB RAM"},
    {"name": "Laptop Backpack 30L", "category": "sports", "price": 1499, "discount_price": None, "stock": 100, "is_featured": False, "description": "Durable 30L backpack with dedicated laptop compartment (fits up to 15.6 inch), multiple pockets, and ergonomic straps.", "short_description": "Fits 15.6\" laptop, water resistant"},
    {"name": "Men's Cotton T-Shirt", "category": "clothing", "price": 599, "discount_price": 399, "stock": 200, "is_featured": True, "description": "Comfortable 100% cotton t-shirt available in multiple colors. Pre-shrunk fabric, regular fit.", "short_description": "100% cotton, regular fit"},
    {"name": "Non-Stick Cookware Set", "category": "home-kitchen", "price": 3499, "discount_price": 2499, "stock": 40, "is_featured": False, "description": "5-piece non-stick cookware set including frying pan, saucepan, and deep pot. PFOA-free coating, suitable for all cooktops.", "short_description": "5-piece PFOA-free set"},
    {"name": "Python Programming Book", "category": "books", "price": 799, "discount_price": None, "stock": 75, "is_featured": False, "description": "Complete guide to Python programming from beginner to advanced. Covers data structures, OOP, web development, and data science.", "short_description": "Beginner to advanced, 500+ pages"},
    {"name": "Yoga Mat Premium", "category": "sports", "price": 1299, "discount_price": 899, "stock": 60, "is_featured": True, "description": "6mm thick premium yoga mat with anti-slip surface, alignment lines, and carrying strap. Eco-friendly TPE material.", "short_description": "6mm thick, anti-slip, eco-friendly"},
    {"name": "Face Moisturizer SPF 50", "category": "beauty", "price": 699, "discount_price": None, "stock": 150, "is_featured": False, "description": "Lightweight daily moisturizer with broad spectrum SPF 50 protection. Suitable for all skin types, non-greasy formula.", "short_description": "SPF 50, all skin types, non-greasy"},
    {"name": "Smart Watch Series 6", "category": "electronics", "price": 8999, "discount_price": 6999, "stock": 25, "is_featured": True, "description": "Feature-packed smartwatch with health monitoring, GPS, 7-day battery, water resistance up to 50m, and 40+ workout modes.", "short_description": "7-day battery, GPS, health monitoring"},
    {"name": "Women's Running Shoes", "category": "sports", "price": 3499, "discount_price": 2799, "stock": 80, "is_featured": True, "description": "Lightweight running shoes with cushioned midsole, breathable mesh upper, and durable rubber outsole. Ideal for road running.", "short_description": "Cushioned, breathable, road running"},
    {"name": "Stainless Steel Water Bottle", "category": "home-kitchen", "price": 799, "discount_price": 599, "stock": 120, "is_featured": False, "description": "1 litre double-walled vacuum insulated bottle. Keeps drinks cold 24 hours and hot 12 hours. BPA-free, leak-proof lid.", "short_description": "1L, keeps cold 24h / hot 12h"},
    {"name": "Linen Formal Shirt", "category": "clothing", "price": 1299, "discount_price": None, "stock": 90, "is_featured": False, "description": "Premium linen formal shirt for men. Slim fit with classic collar, wrinkle-resistant fabric, ideal for office or casual wear.", "short_description": "Slim fit, wrinkle-resistant linen"},
]


class Command(BaseCommand):
    help = "Seed database with sample categories and products"

    def handle(self, *args, **options):
        self.stdout.write("Seeding categories...")
        cat_map = {}
        for c in CATEGORIES:
            obj, _ = Category.objects.get_or_create(slug=c["slug"], defaults={"name": c["name"], "description": c["description"]})
            cat_map[c["slug"]] = obj
            self.stdout.write(f"  ✓ {obj.name}")

        self.stdout.write("Seeding products...")
        for p in PRODUCTS:
            cat = cat_map.get(p["category"])
            if not cat:
                continue
            from django.utils.text import slugify
            slug = slugify(p["name"])
            obj, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": p["name"],
                    "category": cat,
                    "price": p["price"],
                    "discount_price": p.get("discount_price"),
                    "stock": p["stock"],
                    "is_featured": p.get("is_featured", False),
                    "description": p["description"],
                    "short_description": p.get("short_description", ""),
                    "is_active": True,
                }
            )
            action = "created" if created else "already exists"
            self.stdout.write(f"  ✓ {obj.name} ({action})")

        self.stdout.write(self.style.SUCCESS("\n✅ Done! Database seeded successfully."))
        self.stdout.write("   Run: python manage.py createsuperuser  to create an admin account.")
