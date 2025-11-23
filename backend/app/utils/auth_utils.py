from functools import wraps
from flask import session, jsonify
from .enums import UserRole


def login_required(f):
    """
    Decorator that ensures the user is logged in.
    If not logged in, returns 401 JSON response.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Login required"}), 401
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    """
    Decorator that ensures the current user is an admin.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session or session.get("role") != UserRole.ADMIN.value:
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return wrapper


def customer_required(f):
    """
    Decorator that ensures the current user is a customer.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session or session.get("role") != UserRole.CUSTOMER.value:
            return jsonify({"error": "Customer access required"}), 403
        return f(*args, **kwargs)
    return wrapper
