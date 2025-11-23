from flask import Blueprint, request, jsonify, session
from ..services import PaymentManager
from ..models import Booking, Customer
from ..schemas import PaymentCreateSchema
from ..utils import customer_required, admin_required

payment_bp = Blueprint("payments", __name__)
payment_manager = PaymentManager()


# =======================================================
# CUSTOMER — CREATE PAYMENT
# =======================================================
@payment_bp.route("/", methods=["POST"])
@customer_required
def create_payment():
    data = request.get_json(force=True)

    # Validate schema
    schema = PaymentCreateSchema(
        booking_id=data["booking_id"],
        amount=float(data["amount"]),
        method=data["method"],
    )

    # Ensure booking belongs to logged-in customer
    booking = Booking.get_by_id(schema.booking_id)
    if not booking or booking.customer_id != session.get("customer_id"):
        return jsonify({"error": "Invalid booking"}), 403

    payment = payment_manager.create_payment(schema)

    return jsonify({
        "id": payment.id,
        "status": payment.status,
        "amount": payment.amount,
        "method": payment.method
    }), 201


# =======================================================
# CUSTOMER — LIST OWN PAYMENTS
# =======================================================
@payment_bp.route("/my", methods=["GET"])
@customer_required
def my_payments():
    customer_id = session.get("customer_id")

    payments = payment_manager.list_payments_by_customer(customer_id)

    response = []
    for p in payments:
        booking = Booking.get_by_id(p.booking_id)
        response.append({
            "id": p.id,
            "booking_id": p.booking_id,
            "amount": p.amount,
            "status": p.status,
            "method": p.method,
            "reference": p.transaction_reference,
            "vehicle_id": booking.vehicle_id if booking else None
        })

    return jsonify(response)


# =======================================================
# ADMIN — LIST ALL PAYMENTS
# =======================================================
@payment_bp.route("/all", methods=["GET"])
@admin_required
def all_payments():
    payments = payment_manager.get_all()

    response = []
    for p in payments:
        booking = Booking.get_by_id(p.booking_id)
        customer = Customer.get_by_id(booking.customer_id) if booking else None

        response.append({
            "id": p.id,
            "booking_id": p.booking_id,
            "amount": p.amount,
            "status": p.status,
            "method": p.method,
            "reference": p.transaction_reference,
            "customer": customer.name if customer else None
        })

    return jsonify(response)


# =======================================================
# ADMIN — MARK PAYMENT AS PAID
# =======================================================
@payment_bp.route("/<int:payment_id>/pay", methods=["POST"])
@admin_required
def mark_paid(payment_id: int):
    data = request.get_json(force=True) or {}
    reference = data.get("reference")

    payment = payment_manager.mark_paid(payment_id, reference)

    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    return jsonify({
        "message": "Payment marked as paid",
        "payment_id": payment.id,
        "status": payment.status,
        "reference": payment.transaction_reference
    })
