
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "dev-key-change-before-deployment"
)

# Sample food menu
foods = [
    {"id": 1, "name": "Chicken Biryani", "price": 180,
     "emoji": "🍗", "description": "Spicy and delicious biryani"},
    {"id": 2, "name": "Veg Biryani", "price": 120,
     "emoji": "🍚", "description": "Flavourful vegetable biryani"},
    {"id": 3, "name": "Pizza", "price": 200,
     "emoji": "🍕", "description": "Cheesy pizza"},
    {"id": 4, "name": "Burger", "price": 100,
     "emoji": "🍔", "description": "Fresh and tasty burger"},
    {"id": 5, "name": "Dosa", "price": 60,
     "emoji": "🥞", "description": "Crispy South Indian dosa"},
    {"id": 6, "name": "Fried Rice", "price": 140,
     "emoji": "🍜", "description": "Delicious fried rice"},
    {"id": 7, "name": "Sandwich", "price": 80,
     "emoji": "🥪", "description": "Fresh vegetable sandwich"},
    {"id": 8, "name": "Ice Cream", "price": 70,
     "emoji": "🍨", "description": "Sweet and creamy dessert"}
]

# Temporary order storage
orders = []
next_order_id = 1


def get_food(food_id):
    return next(
        (food for food in foods if food["id"] == food_id),
        None
    )


def get_cart_items():
    cart = session.get("cart", {})
    items = []

    for food_id, quantity in cart.items():
        food = get_food(int(food_id))

        if food and quantity > 0:
            item = food.copy()
            item["quantity"] = quantity
            item["subtotal"] = food["price"] * quantity
            items.append(item)

    return items


def cart_total(items):
    return sum(item["subtotal"] for item in items)


@app.context_processor
def common_template_data():
    cart = session.get("cart", {})
    return {"cart_count": sum(cart.values())}


@app.route("/")
def home():
    return render_template("index.html", foods=foods)


@app.route("/menu")
def menu():
    return render_template("menu.html", foods=foods)


@app.route("/add-to-cart/<int:food_id>", methods=["POST"])
def add_to_cart(food_id):
    food = get_food(food_id)

    if not food:
        flash("Food item not found.", "error")
        return redirect(url_for("menu"))

    try:
        quantity = int(request.form.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 0

    if not 1 <= quantity <= 20:
        flash("Choose a quantity between 1 and 20.", "error")
        return redirect(url_for("menu"))

    cart = session.get("cart", {})
    key = str(food_id)
    new_quantity = cart.get(key, 0) + quantity

    if new_quantity > 20:
        flash("Maximum 20 of each food item allowed.", "error")
        return redirect(url_for("menu"))

    cart[key] = new_quantity
    session["cart"] = cart

    flash(f"{food['name']} added to your cart!", "success")
    return redirect(url_for("menu"))


@app.route("/cart")
def cart():
    items = get_cart_items()
    return render_template(
        "cart.html", items=items, total=cart_total(items)
    )


@app.route("/update-cart/<int:food_id>", methods=["POST"])
def update_cart(food_id):
    if not get_food(food_id):
        flash("Food item not found.", "error")
        return redirect(url_for("cart"))

    try:
        quantity = int(request.form.get("quantity", 0))
    except (TypeError, ValueError):
        quantity = 0

    cart = session.get("cart", {})
    key = str(food_id)

    if quantity == 0:
        cart.pop(key, None)
    elif 1 <= quantity <= 20:
        cart[key] = quantity
    else:
        flash("Quantity must be between 0 and 20.", "error")

    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/remove-from-cart/<int:food_id>", methods=["POST"])
def remove_from_cart(food_id):
    cart = session.get("cart", {})
    cart.pop(str(food_id), None)
    session["cart"] = cart
    flash("Item removed from cart.", "success")
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["POST"])
def checkout():
    global next_order_id

    name = request.form.get("customer_name", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    items = get_cart_items()

    if not name or not phone or not address:
        flash("Please complete all checkout fields.", "error")
        return redirect(url_for("cart"))

    if len(name) > 100 or len(phone) > 20 or len(address) > 500:
        flash("One or more fields are too long.", "error")
        return redirect(url_for("cart"))

    if not phone.isdigit() or not 7 <= len(phone) <= 15:
        flash("Enter a valid phone number using digits only.", "error")
        return redirect(url_for("cart"))

    if not items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("menu"))

    order = {
        "id": next_order_id,
        "customer_name": name,
        "phone": phone,
        "address": address,
        "items": items,
        "total": cart_total(items),
        "status": "Order Received",
        "date": datetime.now().strftime("%d-%m-%Y %I:%M %p")
    }

    orders.append(order)
    next_order_id += 1

    session["cart"] = {}
    flash(f"Order #{order['id']} placed successfully!", "success")
    return redirect(url_for("view_orders"))


@app.route("/orders")
def view_orders():
    return render_template("orders.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True)
