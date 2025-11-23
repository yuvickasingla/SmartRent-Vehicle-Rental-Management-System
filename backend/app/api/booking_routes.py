# app/api/booking_routes.py

from flask import Blueprint, request, jsonify, session
from ..services import RentalManager
from ..schemas import BookingCreateSchema
from ..utils import customer_required, admin_required, login_required

booking_bp = Blueprint("bookings", __name__)
rental_manager = RentalManager()


# ============================
# 1) CREATE BOOKING (Customer)
# ============================
@booking_bp.route("/", methods=["POST"])
@customer_required
def create_booking():
    data = request.get_json(force=True)

    # Parse required fields
    try:
        schema = BookingCreateSchema(
            vehicle_id=data["vehicle_id"],
            start_date=data["start_date"],   # must be ISO date string
            end_date=data["end_date"],
            driver_id=data.get("driver_id"),
        )
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    customer_id = session.get("customer_id")

    try:
        booking = rental_manager.create_booking(customer_id, schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "id": booking.id,
        "total_amount": booking.total_amount,
        "status": booking.status
    }), 201


# ==================================
# 2) CUSTOMER — View My Bookings
# ==================================
@booking_bp.route("/my", methods=["GET"])
@customer_required
def my_bookings():
    customer_id = session.get("customer_id")
    bookings = rental_manager.list_bookings_by_customer(customer_id)

    response = [
        {
            "id": b.id,
            "vehicle_id": b.vehicle_id,
            "driver_id": b.driver_id,
            "start_date": b.start_date.isoformat() if b.start_date else None,
            "end_date": b.end_date.isoformat() if b.end_date else None,
            "status": b.status,
            "total_amount": b.total_amount,
        }
        for b in bookings
    ]

    return jsonify(response), 200


# ===============================
# 3) ADMIN — View ALL bookings
# ===============================
@booking_bp.route("/all", methods=["GET"])
@admin_required
def all_bookings():
    bookings = rental_manager.get_all()

    response = [
        {
            "id": b.id,
            "customer_id": b.customer_id,
            "vehicle_id": b.vehicle_id,
            "driver_id": b.driver_id,
            "start_date": b.start_date.isoformat() if b.start_date else None,
            "end_date": b.end_date.isoformat() if b.end_date else None,
            "status": b.status,
            "total_amount": b.total_amount,
        }
        for b in bookings
    ]

    return jsonify(response), 200


# ===============================
# 4) ADMIN — Complete Booking
# ===============================
@booking_bp.route("/<int:booking_id>/complete", methods=["POST"])
@admin_required
def complete_booking(booking_id: int):
    booking = rental_manager.complete_booking(booking_id)

    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify({"message": "Booking completed"}), 200


# ===============================
# 5) ADMIN — Cancel Booking
# ===============================
@booking_bp.route("/<int:booking_id>/cancel", methods=["POST"])
@admin_required
def cancel_booking(booking_id: int):
    booking = rental_manager.cancel_booking(booking_id)

    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify({"message": "Booking cancelled"}), 200
