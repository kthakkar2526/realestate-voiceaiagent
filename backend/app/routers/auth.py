from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import User, Lead
from app.auth_utils import generate_otp, send_otp_sms, create_jwt, verify_jwt

router = APIRouter(prefix="/api/auth")


class SendOtpRequest(BaseModel):
    phone: str


class VerifyOtpRequest(BaseModel):
    phone: str
    otp: str


class ProfileRequest(BaseModel):
    name: str
    email: str


@router.post("/send-otp")
def send_otp(request: SendOtpRequest, db: Session = Depends(get_db)):
    phone = request.phone.strip()
    if not phone:
        raise HTTPException(status_code=400, detail="Phone number required")

    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        user = User(phone=phone)
        db.add(user)

    otp = generate_otp()
    user.otp_code = otp
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=5)
    db.commit()

    send_otp_sms(phone, otp)
    return {"message": "OTP sent", "phone": phone}


@router.post("/verify-otp")
def verify_otp(request: VerifyOtpRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == request.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.otp_code or user.otp_code != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if user.otp_expires_at and user.otp_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    # Clear OTP
    user.otp_code = None
    user.otp_expires_at = None
    db.commit()

    token = create_jwt(user.id, user.phone)
    return {
        "token": token,
        "user": {
            "id": user.id,
            "phone": user.phone,
            "name": user.name,
            "email": user.email,
        },
    }


@router.get("/me")
def get_me(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = verify_jwt(authorization.replace("Bearer ", ""))
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "phone": user.phone,
        "name": user.name,
        "email": user.email,
    }


@router.post("/profile")
def update_profile(request: ProfileRequest, authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = verify_jwt(authorization.replace("Bearer ", ""))
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = request.name.strip()
    user.email = request.email.strip()

    # Create a lead so the sales team can see this person immediately
    existing_lead = db.query(Lead).filter(Lead.user_id == user.id).first()
    if not existing_lead:
        lead = Lead(
            session_id=f"user-{user.id}",
            user_id=user.id,
            name=user.name,
            phone=user.phone,
            email=user.email,
        )
        db.add(lead)
    else:
        existing_lead.name = user.name
        existing_lead.email = user.email
        existing_lead.phone = user.phone

    db.commit()

    return {
        "id": user.id,
        "phone": user.phone,
        "name": user.name,
        "email": user.email,
    }
