from flask import Flask
from .database import db
from .api.auth_routes import auth_bp
from .api.vehicle_routes import vehicle_bp
from .api.booking_routes import booking_bp
from .api.driver_routes import driver_bp
from .api.payment_routes import payment_bp
from .api.maintenance_routes import maintenance_bp
from .api.customer_routes import customer_bp


def create_app() -> Flask:
    """
    Application factory: creates and configures the Flask app.

    We set up Flask, configure the database, register blueprints (routes),
    and return the app instance.
    """
    app = Flask(__name__)
    from flask_cors import CORS

    CORS(
        app,
        supports_credentials=True,
        origins=["http://127.0.0.1:8000"]   # <-- frontend
    )


    # Secret key for sessions (required for login session management).
    app.config["SECRET_KEY"] = "super-secret-key-change-later"

    # Initialize our custom database object (mysql-connector-based).
    db.init_app(app)

    # Register blueprints for different parts of the API.
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(vehicle_bp, url_prefix="/vehicles")
    app.register_blueprint(booking_bp, url_prefix="/bookings")
    app.register_blueprint(driver_bp, url_prefix="/drivers")
    app.register_blueprint(payment_bp, url_prefix="/payments")
    app.register_blueprint(maintenance_bp, url_prefix="/maintenance")
    app.register_blueprint(customer_bp, url_prefix="/customers")

    @app.route("/")
    def index():
        return {
            "message": "Vehicle Rental Backend is running",
            "endpoints": [
                "/auth/login",
                "/auth/register_customer",
                "/vehicles/",
                "/bookings/",
            ],
        }

    return app
