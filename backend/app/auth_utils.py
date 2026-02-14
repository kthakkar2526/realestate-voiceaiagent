import random
import jwt
from datetime import datetime, timedelta, timezone
from twilio.rest import Client
from app.config import settings


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def send_otp_sms(phone: str, otp: str):
    if not settings.TWILIO_ACCOUNT_SID:
        print(f"[DEV MODE] OTP for {phone}: {otp}")
        return
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f"Your PropertyAI verification code is: {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone,
    )


def create_jwt(user_id: int, phone: str) -> str:
    payload = {
        "user_id": user_id,
        "phone": phone,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def verify_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
