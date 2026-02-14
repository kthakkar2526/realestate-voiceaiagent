from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.config import settings
from app.models import Lead

router = APIRouter(prefix="/api")


def verify_admin(authorization: str = Header(...)):
    if authorization != f"Bearer {settings.ADMIN_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/leads", dependencies=[Depends(verify_admin)])
def list_leads(db: Session = Depends(get_db)):
    leads = (
        db.query(Lead)
        .options(joinedload(Lead.requirements))
        .order_by(Lead.created_at.desc())
        .all()
    )
    return [
        {
            "id": l.id,
            "session_id": l.session_id,
            "name": l.name,
            "phone": l.phone,
            "email": l.email,
            "created_at": str(l.created_at),
            "requirements": [
                {
                    "budget_min": r.budget_min,
                    "budget_max": r.budget_max,
                    "city": r.city,
                    "location_pref": r.location_pref,
                    "property_type": r.property_type,
                    "bhk_min": r.bhk_min,
                    "bhk_max": r.bhk_max,
                    "amenities": r.amenities,
                    "additional_notes": r.additional_notes,
                }
                for r in l.requirements
            ],
        }
        for l in leads
    ]


@router.get("/leads/{lead_id}", dependencies=[Depends(verify_admin)])
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = (
        db.query(Lead)
        .options(joinedload(Lead.requirements), joinedload(Lead.bookings))
        .filter(Lead.id == lead_id)
        .first()
    )
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead
