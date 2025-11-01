from flask import Blueprint, render_template, jsonify, request
from .models import Product
from . import db
import stripe

main = Blueprint("main", __name__)

@main.route("/")
def index():
    # Load all products and render to HTML
    products = Product.query.all()
    return render_template("index.html", products=products)

@main.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    # Parse received data and check if product exists in db
    data = request.json
    product_id = data.get("product_id")
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Start Stripe session using a credit card and relocate if fail/pass
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": product.name},
                "unit_amount": product.price,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:5000/success",
        cancel_url="http://localhost:5000/",
    )
    return jsonify({"id": session.id})

@main.route("/success")
def success():
    return "<h1>Payment successful!</h1>"
