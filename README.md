# 🛍️ ShopEase – Django Ecommerce Website

A fully featured, deploy-ready ecommerce website built with **Django 5**, **Tailwind CSS**, **SQLite**, and **Stripe** payments.

---

## ✨ Features

- 🏪 Product catalogue with categories, filters, search & pagination
- 🛒 Session-based cart (works without login)
- ❤️ Wishlist
- 💳 Stripe payment gateway (card payments)
- 📦 Order management with status tracking
- 👤 Custom user accounts (register / login / profile)
- ⭐ Product reviews & ratings
- 🔖 Product image gallery
- 🎛️ Django Admin panel
- 📱 Fully responsive (mobile-first Tailwind CSS)
- 🔒 Secure `.env` configuration
- 🌱 Database seeder for sample data

---

## 🚀 Quick Start

### 1. Clone / extract the project

```bash
cd ecommerce_project
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env` and fill in your values:

```bash
cp .env .env.local   # optional – keep original as template
```

Edit `.env`:
```
SECRET_KEY=your-very-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

> Get Stripe keys free at https://dashboard.stripe.com/apikeys

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Seed sample data

```bash
python manage.py seed_data
```

### 7. Create admin account

```bash
python manage.py createsuperuser
```

### 8. Run the server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000 🎉

---

## 🔐 Stripe Test Cards

| Card Number | Description |
|---|---|
| `4242 4242 4242 4242` | Success |
| `4000 0000 0000 0002` | Card declined |
| `4000 0025 0000 3155` | Requires authentication |

Use any future expiry date and any 3-digit CVC.

---

## 📁 Project Structure

```
ecommerce_project/
├── ecommerce/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/              # Products, cart, wishlist
│   ├── models.py       # Category, Product, Review, Wishlist
│   ├── views.py
│   ├── urls.py
│   └── management/commands/seed_data.py
├── accounts/           # Custom user auth
│   ├── models.py       # CustomUser
│   ├── views.py
│   └── forms.py
├── orders/             # Checkout & order management
│   ├── models.py       # Order, OrderItem, Coupon
│   └── views.py
├── payments/           # Stripe integration
│   ├── views.py
│   └── urls.py
├── templates/          # All HTML templates
│   ├── base.html
│   ├── store/
│   ├── accounts/
│   ├── orders/
│   ├── payments/
│   └── partials/
├── static/             # CSS, JS, images
├── media/              # User-uploaded files
├── .env                # Environment variables (edit this!)
├── requirements.txt
└── manage.py
```

---

## 🌐 Deploy to Production

### Checklist
- [ ] Set `DEBUG=False` in `.env`
- [ ] Set a strong `SECRET_KEY`
- [ ] Add your domain to `ALLOWED_HOSTS`
- [ ] Run `python manage.py collectstatic`
- [ ] Switch to Stripe **live** keys
- [ ] Set up Stripe webhook pointing to `https://yourdomain.com/payments/webhook/`

### Deploy options
- **Railway** – `railway up` (easiest, free tier)
- **Render** – Connect GitHub repo, add env vars
- **Heroku** – `git push heroku main`
- **VPS** – Nginx + Gunicorn + systemd

---

## 🛠️ Admin Panel

Visit http://127.0.0.1:8000/admin/

- Add/edit products and categories
- Manage orders and update status
- View customer accounts
- Add product images via inline editor

---

## 📧 Email (Order Confirmations)

For development, emails print to the console (default).
For production, configure Gmail or SendGrid in `.env`:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

Built with ❤️ using Django + Tailwind CSS + Stripe
