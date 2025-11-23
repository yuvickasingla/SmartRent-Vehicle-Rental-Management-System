from flask import Blueprint, request, jsonify
from ..services import DriverManager
from ..schemas import DriverCreateSchema
from ..utils import admin_required, login_required

driver_bp = Blueprint("drivers", __name__)
driver_manager = DriverManager()


# =======================================================
# GET ALL DRIVERS (Admin + Logged in users)
# =======================================================
@driver_bp.route("/", methods=["GET"])
@login_required
def list_drivers():
    drivers = driver_manager.get_all()

    response = [
        {
            "id": d.id,
            "name": d.name,
            "phone": d.phone,
            "license_number": d.license_number,
            "is_available": bool(d.is_available),
        }
        for d in drivers
    ]

    return jsonify(response)


# =======================================================
# GET AVAILABLE DRIVERS
# =======================================================
@driver_bp.route("/available", methods=["GET"])
@login_required
def available_drivers():
    drivers = driver_manager.list_available()

    response = [
        {
            "id": d.id,
            "name": d.name,
            "phone": d.phone,
        }
        for d in drivers
    ]
    return jsonify(response)


# =======================================================
# ADD DRIVER (Admin)
# =======================================================
@driver_bp.route("/", methods=["POST"])
@admin_required
def create_driver():
    data = request.get_json(force=True)

    schema = DriverCreateSchema(
        name=data.get("name", ""),
        phone=data.get("phone", ""),
        license_number=data.get("license_number", ""),
    )

    try:
        driver = driver_manager.create_driver(schema)
        return jsonify({"id": driver.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =======================================================
# UPDATE DRIVER (Admin)
# =======================================================
@driver_bp.route("/<int:driver_id>", methods=["PUT"])
@admin_required
def update_driver(driver_id: int):
    data = request.get_json(force=True)
    driver = driver_manager.update_driver(driver_id, data)

    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    return jsonify({"message": "Driver updated"})


# =======================================================
# DELETE DRIVER (Admin)
# =======================================================
@driver_bp.route("/<int:driver_id>", methods=["DELETE"])
@admin_required
def delete_driver(driver_id: int):
    success = driver_manager.delete(driver_id)

    if not success:
        return jsonify({"error": "Driver not found"}), 404

    return jsonify({"message": "Driver deleted"})
