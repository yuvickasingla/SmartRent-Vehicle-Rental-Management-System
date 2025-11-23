from flask import Blueprint, request, jsonify, session
from ..models import Customer
from ..schemas import CustomerUpdateSchema
from ..utils import customer_required, admin_required

customer_bp = Blueprint("customers", __name__)


# =======================================================
# GET CUSTOMER PROFILE
# =======================================================
@customer_bp.route("/<int:customer_id>", methods=["GET"])
@customer_required
def get_customer(customer_id):
    # Customers can only view their own profile
    if session.get("customer_id") != customer_id:
        return jsonify({"error": "You can only view your own profile"}), 403

    customer = Customer.get_by_id(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify({
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "license_number": customer.license_number
    })


# =======================================================
# UPDATE CUSTOMER PROFILE
# =======================================================
@customer_bp.route("/<int:customer_id>", methods=["PUT"])
@customer_required
def update_customer(customer_id):

    # Customer can only update their own profile
    if session.get("customer_id") != customer_id:
        return jsonify({"error": "You can only update your own profile"}), 403

    data = request.get_json(force=True)

    schema = CustomerUpdateSchema(
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
        license_number=data.get("license_number"),
    )

    customer = Customer.get_by_id(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    # Apply updates
    if schema.name is not None:
        customer.name = schema.name
    if schema.email is not None:
        customer.email = schema.email
    if schema.phone is not None:
        customer.phone = schema.phone
    if schema.license_number is not None:
        customer.license_number = schema.license_number

    try:
        customer.save()
        return jsonify({"message": "Profile updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
