import json
from sqlalchemy.orm import Session
from app.models import Property, Lead, Requirement, Booking
from app.notifications import send_booking_notifications

# --- Tool Declarations for Gemini ---

search_properties_declaration = {
    "name": "search_properties",
    "description": "Search the property database for listings matching the user's requirements.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City to search in"},
            "location": {"type": "string", "description": "Specific area/locality (optional)"},
            "property_type": {"type": "string", "enum": ["apartment", "villa", "plot", "independent_house"]},
            "bhk_min": {"type": "integer", "description": "Minimum BHK count"},
            "bhk_max": {"type": "integer", "description": "Maximum BHK count"},
            "budget_min": {"type": "number", "description": "Minimum budget"},
            "budget_max": {"type": "number", "description": "Maximum budget"},
            "amenities": {"type": "array", "items": {"type": "string"}, "description": "Desired amenities"},
        },
        "required": ["city"],
    },
}

save_requirements_declaration = {
    "name": "save_requirements",
    "description": "Save or update the user's property requirements to the database.",
    "parameters": {
        "type": "object",
        "properties": {
            "budget_min": {"type": "number"},
            "budget_max": {"type": "number"},
            "city": {"type": "string"},
            "location_pref": {"type": "string"},
            "property_type": {"type": "string"},
            "bhk_min": {"type": "integer"},
            "bhk_max": {"type": "integer"},
            "amenities": {"type": "array", "items": {"type": "string"}},
            "additional_notes": {"type": "string"},
        },
        "required": [],
    },
}

book_visit_declaration = {
    "name": "book_visit",
    "description": "Book a property visit. Call after confirming property ID, date, and time with the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "property_id": {"type": "integer", "description": "ID of the property to visit"},
            "visit_date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
            "visit_time": {"type": "string", "description": "Time like '10:00 AM'"},
        },
        "required": ["property_id", "visit_date", "visit_time"],
    },
}

save_contact_declaration = {
    "name": "save_contact",
    "description": "Save the user's contact information (name, phone, email).",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "phone": {"type": "string"},
            "email": {"type": "string"},
        },
        "required": ["name"],
    },
}

get_property_details_declaration = {
    "name": "get_property_details",
    "description": "Get full details of a specific property by ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "property_id": {"type": "integer"},
        },
        "required": ["property_id"],
    },
}

ALL_DECLARATIONS = [
    search_properties_declaration,
    save_requirements_declaration,
    book_visit_declaration,
    save_contact_declaration,
    get_property_details_declaration,
]


# --- Tool Execution Functions ---

def execute_search_properties(db: Session, session_id: str, **kwargs) -> dict:
    query = db.query(Property).filter(Property.status == "available")
    if kwargs.get("city"):
        query = query.filter(Property.city.ilike(f"%{kwargs['city']}%"))
    if kwargs.get("location"):
        query = query.filter(Property.location.ilike(f"%{kwargs['location']}%"))
    if kwargs.get("property_type"):
        query = query.filter(Property.property_type == kwargs["property_type"])
    if kwargs.get("budget_min"):
        query = query.filter(Property.price >= kwargs["budget_min"])
    if kwargs.get("budget_max"):
        query = query.filter(Property.price <= kwargs["budget_max"])
    if kwargs.get("bhk_min"):
        query = query.filter(Property.bhk >= kwargs["bhk_min"])
    if kwargs.get("bhk_max"):
        query = query.filter(Property.bhk <= kwargs["bhk_max"])
    results = query.limit(5).all()
    return {"properties": [p.to_dict() for p in results], "count": len(results)}


def execute_save_requirements(db: Session, session_id: str, **kwargs) -> dict:
    lead = db.query(Lead).filter(Lead.session_id == session_id).first()
    if not lead:
        lead = Lead(session_id=session_id)
        db.add(lead)
        db.flush()

    req = db.query(Requirement).filter(Requirement.lead_id == lead.id).first()
    if not req:
        req = Requirement(lead_id=lead.id)
        db.add(req)

    for field in ["budget_min", "budget_max", "city", "location_pref", "property_type",
                  "bhk_min", "bhk_max", "additional_notes"]:
        if kwargs.get(field) is not None:
            setattr(req, field, kwargs[field])
    if kwargs.get("amenities"):
        req.amenities = json.dumps(kwargs["amenities"])

    db.commit()
    return {"success": True, "message": "Requirements saved."}


def execute_book_visit(db: Session, session_id: str, **kwargs) -> dict:
    lead = db.query(Lead).filter(Lead.session_id == session_id).first()
    if not lead:
        return {"error": "Please provide your contact details first."}
    if not lead.name or not lead.phone:
        return {"error": "We need your name and phone number before booking."}

    prop = db.query(Property).filter(Property.id == kwargs["property_id"]).first()
    if not prop:
        return {"error": "Property not found."}

    booking = Booking(
        lead_id=lead.id,
        property_id=kwargs["property_id"],
        visit_date=kwargs["visit_date"],
        visit_time=kwargs["visit_time"],
    )
    db.add(booking)
    db.commit()

    # Send notifications (email + WhatsApp)
    send_booking_notifications(
        lead, prop.title, kwargs["visit_date"], kwargs["visit_time"], booking.id
    )

    return {"success": True, "booking_id": booking.id, "property_title": prop.title,
            "visit_date": kwargs["visit_date"], "visit_time": kwargs["visit_time"]}


def execute_save_contact(db: Session, session_id: str, **kwargs) -> dict:
    lead = db.query(Lead).filter(Lead.session_id == session_id).first()
    if not lead:
        lead = Lead(session_id=session_id)
        db.add(lead)

    if kwargs.get("name"):
        lead.name = kwargs["name"]
    if kwargs.get("phone"):
        lead.phone = kwargs["phone"]
    if kwargs.get("email"):
        lead.email = kwargs["email"]

    db.commit()
    return {"success": True, "message": "Contact info saved."}


def execute_get_property_details(db: Session, session_id: str, **kwargs) -> dict:
    prop = db.query(Property).filter(Property.id == kwargs["property_id"]).first()
    if not prop:
        return {"error": "Property not found."}
    return {"property": prop.to_dict()}


TOOL_REGISTRY = {
    "search_properties": execute_search_properties,
    "save_requirements": execute_save_requirements,
    "book_visit": execute_book_visit,
    "save_contact": execute_save_contact,
    "get_property_details": execute_get_property_details,
}
