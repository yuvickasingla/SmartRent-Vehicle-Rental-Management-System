# app/services/booking_manager.py
from app.models.booking import Booking
from .base_service import BaseService


class BookingManager(BaseService):
    def list_bookings(self):
        conn = self.get_connection()
        if conn is None:
            return []
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM bookings")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Booking(**row).to_dict() for row in rows]

    def get_booking(self, booking_id: int):
        conn = self.get_connection()
        if conn is None:
            return None
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return Booking(**row).to_dict() if row else None
