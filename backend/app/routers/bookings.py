from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.config import settings
from app.models import Booking, Lead, Property
from app.schemas import BookingUpdate

router = APIRouter(prefix="/api")


def verify_admin(authorization: str = Header(...)):
    if authorization != f"Bearer {settings.ADMIN_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/bookings", dependencies=[Depends(verify_admin)])
def list_bookings(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Booking).options(joinedload(Booking.lead), joinedload(Booking.property))
    if status:
        query = query.filter(Booking.status == status)
    bookings = query.order_by(Booking.created_at.desc()).all()
    return [
        {
            "id": b.id,
            "lead_name": b.lead.name,
            "lead_phone": b.lead.phone,
            "property_title": b.property.title,
            "property_id": b.property_id,
            "visit_date": b.visit_date,
            "visit_time": b.visit_time,
            "status": b.status,
            "created_at": str(b.created_at),
        }
        for b in bookings
    ]


@router.patch("/bookings/{booking_id}", dependencies=[Depends(verify_admin)])
def update_booking(booking_id: int, data: BookingUpdate, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = data.status
    db.commit()
    return {"message": f"Booking {booking_id} updated to {data.status}"}
