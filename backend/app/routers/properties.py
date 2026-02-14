from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.models import Property
from app.schemas import PropertyCreate, PropertyUpdate

router = APIRouter(prefix="/api")


def verify_admin(authorization: str = Header(...)):
    if authorization != f"Bearer {settings.ADMIN_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/properties")
def list_properties(city: str | None = None, property_type: str | None = None,
                    status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Property)
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if status:
        query = query.filter(Property.status == status)
    return query.order_by(Property.created_at.desc()).all()


@router.get("/properties/{property_id}")
def get_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop


@router.post("/properties", dependencies=[Depends(verify_admin)])
def create_property(data: PropertyCreate, db: Session = Depends(get_db)):
    prop = Property(**data.model_dump())
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop


@router.put("/properties/{property_id}", dependencies=[Depends(verify_admin)])
def update_property(property_id: int, data: PropertyUpdate, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(prop, field, value)
    db.commit()
    db.refresh(prop)
    return prop


@router.delete("/properties/{property_id}", dependencies=[Depends(verify_admin)])
def delete_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(prop)
    db.commit()
    return {"message": "Deleted"}
