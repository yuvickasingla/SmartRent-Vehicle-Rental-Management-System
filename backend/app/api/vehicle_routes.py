from flask import Blueprint, request, jsonify
from ..services import VehicleManager
from ..schemas import VehicleCreateSchema
from ..utils import admin_required, login_required

vehicle_bp = Blueprint("vehicles", __name__)
vehicle_manager = VehicleManager()


# ==========================
# GET ALL VEHICLES (admin)
# ==========================
@vehicle_bp.route("/", methods=["GET"])
@login_required
def list_vehicles():
    vehicles = vehicle_manager.get_all()
    response = [
        {
            "id": v.id,
            "registration_number": v.registration_number,
            "brand": v.brand,
            "model": v.model,
            "daily_rate": v.daily_rate,
            "vehicle_type": v.vehicle_type,
            "status": v.status,
        }
        for v in vehicles
    ]
    return jsonify(response)


# ==========================
# GET SINGLE VEHICLE
# ==========================
@vehicle_bp.route("/<int:vehicle_id>", methods=["GET"])
@login_required
def get_vehicle(vehicle_id):
    v = vehicle_manager.get_by_id(vehicle_id)
    if not v:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify({
        "id": v.id,
        "registration_number": v.registration_number,
        "brand": v.brand,
        "model": v.model,
        "daily_rate": v.daily_rate,
        "vehicle_type": v.vehicle_type,
        "status": v.status,
        "seats": v.seats,
        "transmission": v.transmission,
        "engine_cc": v.engine_cc,
        "has_gear": v.has_gear,
    })


# ==========================
# GET AVAILABLE VEHICLES
# ==========================
@vehicle_bp.route("/available", methods=["GET"])
@login_required
def list_available():
    vehicles = vehicle_manager.list_available()
    response = [
        {
            "id": v.id,
            "registration_number": v.registration_number,
            "brand": v.brand,
            "model": v.model,
            "daily_rate": v.daily_rate,
        }
        for v in vehicles
    ]
    return jsonify(response)


# ==========================
# ADD VEHICLE
# ==========================
@vehicle_bp.route("/", methods=["POST"])
@admin_required
def create_vehicle():
    data = request.get_json(force=True)

    # safe defaults
    schema = VehicleCreateSchema(
        registration_number=data.get("registration_number", ""),
        brand=data.get("brand", ""),
        model=data.get("model", ""),
        daily_rate=float(data.get("daily_rate", 0)),
        vehicle_type=data.get("vehicle_type", "car").lower(),
        seats=data.get("seats"),
        transmission=data.get("transmission"),
        engine_cc=data.get("engine_cc"),
        has_gear=data.get("has_gear"),
    )

    try:
        vehicle = vehicle_manager.create_vehicle(schema)
        return jsonify({"id": vehicle.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ==========================
# UPDATE VEHICLE
# ==========================
@vehicle_bp.route("/<int:vehicle_id>", methods=["PUT"])
@admin_required
def update_vehicle(vehicle_id: int):
    data = request.get_json(force=True)
    vehicle = vehicle_manager.update_vehicle(vehicle_id, data)

    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify({"message": "Vehicle updated"})


# ==========================
# DELETE VEHICLE
# ==========================
@vehicle_bp.route("/<int:vehicle_id>", methods=["DELETE"])
@admin_required
def delete_vehicle(vehicle_id: int):
    success = vehicle_manager.delete(vehicle_id)

    if not success:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify({"message": "Vehicle deleted"})
