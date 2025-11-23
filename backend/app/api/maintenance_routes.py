# app/api/maintenance_routes.py

from flask import Blueprint, request, jsonify
from ..services import MaintenanceManager
from ..schemas import MaintenanceCreateSchema
from ..utils import admin_required

maintenance_bp = Blueprint("maintenance", __name__)
maintenance_manager = MaintenanceManager()


# ================================
# 1) LIST ALL MAINTENANCE RECORDS
# ================================
@maintenance_bp.route("/", methods=["GET"])
@admin_required
def list_maintenance():
    records = maintenance_manager.get_all()

    response = [
        {
            "id": r.id,
            "vehicle_id": r.vehicle_id,
            "description": r.description,
            "cost": r.cost,
            "status": r.status,
            "scheduled_date": r.scheduled_date.isoformat() if r.scheduled_date else None,
            "completed_date": r.completed_date.isoformat() if r.completed_date else None,
        }
        for r in records
    ]

    return jsonify(response), 200


# ================================
# 2) CREATE MAINTENANCE RECORD
# ================================
@maintenance_bp.route("/", methods=["POST"])
@admin_required
def create_maintenance():
    data = request.get_json(force=True)

    schema = MaintenanceCreateSchema(
        vehicle_id=data["vehicle_id"],
        description=data["description"],
    )

    record = maintenance_manager.create_record(schema)

    return jsonify({
        "id": record.id,
        "status": record.status,
        "message": "Maintenance record created"
    }), 201


# ================================
# 3) COMPLETE MAINTENANCE RECORD
# ================================
@maintenance_bp.route("/<int:record_id>/complete", methods=["POST"])
@admin_required
def complete_maintenance(record_id: int):
    data = request.get_json(force=True)
    cost = float(data.get("cost", 0.0))

    record = maintenance_manager.complete_record(record_id, cost)

    if not record:
        return jsonify({"error": "Record not found"}), 404

    return jsonify({
        "message": "Maintenance completed",
        "id": record.id,
        "cost": record.cost,
        "status": record.status
    })
