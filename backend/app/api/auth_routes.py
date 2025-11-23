from flask import Blueprint, request, jsonify, session
from ..services import AuthManager
from ..schemas import UserLoginSchema, UserRegisterCustomerSchema
from ..utils import UserRole

auth_bp = Blueprint("auth", __name__)
auth_manager = AuthManager()


# ---------------------------------------------------
# CUSTOMER REGISTRATION
# ---------------------------------------------------
@auth_bp.route("/register_customer", methods=["POST"])
def register_customer():
    try:
        data = request.get_json(force=True)

        schema = UserRegisterCustomerSchema(
            username=data.get("username"),
            password=data.get("password"),
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            license_number=data.get("license_number"),
        )

        user = auth_manager.register_customer(schema)

        return jsonify({
            "id": user.id,
            "role": user.role,
            "message": "Customer registered successfully"
        }), 201

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400



# ---------------------------------------------------
# LOGIN (ADMIN + CUSTOMER)
# ---------------------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)

    schema = UserLoginSchema(
        username=data.get("username"),
        password=data.get("password"),
    )

    user = auth_manager.authenticate(schema)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # Save login session
    session.clear()
    session["user_id"] = user.id
    session["role"] = user.role
    session["customer_id"] = user.customer_id

    # Redirect location based on role
    redirect_url = (
        "/admin/dashboard.html" if user.role == UserRole.ADMIN.value
        else "/customer/dashboard.html"
    )

    return jsonify({
        "message": "Login successful",
        "role": user.role,
        "user_id": user.id,
        "customer_id": user.customer_id,
        "redirect": redirect_url
    }), 200



# ---------------------------------------------------
# LOGIN STATUS CHECK  (THIS FIXES YOUR REDIRECT ISSUE)
# ---------------------------------------------------
@auth_bp.route("/login", methods=["GET"])
def check_login():
    user_id = session.get("user_id")
    role = session.get("role")
    customer_id = session.get("customer_id")

    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    return jsonify({
        "message": "Logged in",
        "user_id": user_id,
        "role": role,
        "customer_id": customer_id
    }), 200



# ---------------------------------------------------
# LOGOUT
# ---------------------------------------------------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200



# ---------------------------------------------------
# LIST CUSTOMERS (ADMIN)
# ---------------------------------------------------
@auth_bp.route("/customers", methods=["GET"])
def list_customers():
    customers = auth_manager.list_customers()

    result = [
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "license_number": c.license_number,
        }
        for c in customers
    ]

    return jsonify(result), 200
