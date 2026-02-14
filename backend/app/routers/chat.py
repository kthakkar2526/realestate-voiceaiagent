from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChatRequest, ChatResponse
from app.agent.engine import agent
from app.auth_utils import verify_jwt
from app.models import Lead, User

router = APIRouter(prefix="/api")


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, authorization: str = Header(None), db: Session = Depends(get_db)):
    # Link session to authenticated user if token provided
    user_id = None
    if authorization and authorization.startswith("Bearer "):
        payload = verify_jwt(authorization.replace("Bearer ", ""))
        if payload:
            user_id = payload.get("user_id")
            user = db.query(User).filter(User.id == user_id).first()

            lead = db.query(Lead).filter(Lead.session_id == request.session_id).first()
            if lead and not lead.user_id and user_id and user:
                # Existing lead, link to user
                lead.user_id = user_id
                lead.phone = user.phone
                if user.name:
                    lead.name = user.name
                if user.email:
                    lead.email = user.email
                db.commit()
            elif not lead and user:
                # First message — check if user already has a lead from profile setup
                existing_lead = db.query(Lead).filter(Lead.user_id == user_id).first()
                if existing_lead:
                    # Update the profile-created lead with this chat session_id
                    existing_lead.session_id = request.session_id
                    db.commit()

    # Pass authenticated user info so the agent knows who it's talking to
    user_info = None
    if user_id:
        u = db.query(User).filter(User.id == user_id).first()
        if u:
            user_info = {"name": u.name, "phone": u.phone, "email": u.email}

    result = await agent.handle_message(
        session_id=request.session_id,
        user_message=request.message,
        db=db,
        user_info=user_info,
    )
    return ChatResponse(
        message=result.message,
        properties=result.properties,
        booking=result.booking,
    )
