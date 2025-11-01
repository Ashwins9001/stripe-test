from flask import Blueprint, render_template, jsonify, request
from .models import Product
from . import db
import stripe
import os

main = Blueprint("main", __name__)

# Set Stripe API key from environment
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")  # Add this to your .env

@main.route("/")
def index():
    # Load all products and render to HTML
    products = Product.query.all()
    return render_template("index.html", products=products)

@main.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = request.json
    product_id = data.get("product_id")
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if product.inventory <= 0:
        return jsonify({"error": "Product out of stock"}), 400

    # Start Stripe session and pass product ID in metadata
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
        metadata={"product_id": str(product.id)}  # Important for webhook
    )
    return jsonify({"id": session.id})

@main.route("/success")
def success():
    return "<h1>Payment successful!</h1>"

@main.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Retrieve product ID from metadata
        product_id = session.get("metadata", {}).get("product_id")
        if product_id:
            product = Product.query.get(int(product_id))
            if product and product.inventory > 0:
                product.inventory -= 1
                db.session.commit()

    return jsonify(success=True)
