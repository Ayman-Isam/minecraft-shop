# Minecraft-Shop

A Django web application built for a Minecraft server shared with friends, letting players redeem diamond deposits for site balance, browse and wishlist items, and place orders for in-game delivery at specific `X` and `Z` coordinates.

## How It Works (In-Game + Web Flow)

1. **Deposit Diamonds In-Game**: A player places diamonds into a designated chest on the Minecraft server and presses a button.
2. **Plugin Transfers & Issues Code**: The companion Minecraft plugin moves the diamonds into the shop owner's chest and generates a redeem code.
3. **Redeem for Balance**: The player enters the code in the cart on **MC-Shop** to add diamonds to their account balance.
4. **Shop & Coordinate Delivery**: Players browse/filter items, manage wishlists and carts, and check out using their diamond balance along with their `X` and `Z` coordinates and shipping speed (`standard-shipping` or `express-shipping`).
5. **Fulfillment & Refunds**: Players view their orders in-app, while superusers can view all orders and cancel/refund orders back to a player's diamond balance.

## Features

- **Filterable Item Catalog**: Paginated home view (`HomePageView`, 6 items per page) with filters for category, price range, and stock status, plus item detail pages.
- **Admin Item Management**: Superuser-only views to create, update, and delete items (`ItemCreateView`, `ItemUpdateView`, `ItemDeleteView`).
- **Account Registration & Email Verification**: Sign-up and login with UUID-token email verification via `Profile`, plus password reset views.
- **Diamond Balance & Redeem Codes**: Redeem codes in the cart to top up a user's `Profile` balance, backed by a Django REST Framework `RedeemViewSet` endpoint for plugin/API integration.
- **Wishlist & Shopping Cart**: Add items, adjust quantities (increment, decrement, update, remove), and move items from wishlist to cart.
- **Checkout & Order Management**:
  - Deducts total cost from the player's diamond balance and records `X` and `Z` coordinates plus estimated delivery dates (3 days for standard, 1 day for express).
  - Superusers can inspect all orders and cancel/refund unfulfilled orders back to the user's balance.

## Tech Stack

- **Backend**: Django & Django REST Framework
- **Database**: SQLite (default Django setup)
- **Templates**: Django HTML Templates (`home.html`, `cart.html`, `wishlist.html`, `orders.html`, `item_detail.html`, etc.)

## Local Setup

## Setup & Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd minecraft-shop
```

### 2. Create a Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables & Email

Your `core/settings.py` reads configuration from environment variables:

- `SECRET_KEY` — Django secret key
- `DEBUG` — Set in your environment (note: `os.environ.get('DEBUG')` returns a string, so keep it unset or handle boolean parsing carefully in production)
- `SERVER_URL` — Hostname of your deployed server (e.g., `cantankerousally.pythonanywhere.com`), added alongside `localhost` and `127.0.0.1` in `ALLOWED_HOSTS`
- `EMAIL_HOST` — SMTP server hostname
- `EMAIL_PORT` — SMTP server port (e.g., `587`)
- `EMAIL_USE_TLS` — TLS setting for SMTP
- `EMAIL_HOST_USER` — Sender email address
- `EMAIL_HOST_PASSWORD` — Email account password or app password

### 4. Run Migrations & Create a Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Your superuser account unlocks item creation/editing/deletion, viewing all orders, and refunding orders.

### 5. Run the Development Server

```bash
python manage.py runserver
```