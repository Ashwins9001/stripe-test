import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import stripe

# Initialize SQLAlchemy globally
db = SQLAlchemy()

def create_app():
    """Flask application factory pattern."""
    # Load .env variables (for local dev)
    load_dotenv()

    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data/products.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    db.init_app(app)

    # Stripe configuration
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # Server-side only (secret key)

    # Register blueprint(s)
    from .routes import main
    app.register_blueprint(main)

    # Expose the publishable key to templates globally
    @app.context_processor
    def inject_stripe_key():
        return {"stripe_publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY", "")}

    # Create tables and seed initial products if empty
    with app.app_context():
        from .models import Product
        db.create_all()
        if Product.query.count() == 0:
            db.session.add_all([
                Product(name="Widget A", price=1000, inventory=5),
                Product(name="Widget B", price=1500, inventory=3),
                Product(name="Widget C", price=2000, inventory=10)
            ])
            db.session.commit()

    return app
