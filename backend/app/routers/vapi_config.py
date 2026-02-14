"""
Returns Vapi assistant configuration.
The frontend calls this to get the assistant config for starting voice calls.
"""

from fastapi import APIRouter, Request
from app.config import settings

router = APIRouter(prefix="/api/vapi")


def get_assistant_config(server_url: str) -> dict:
    """Build Vapi assistant configuration with our tools."""
    return {
        "name": "PropertyAI Voice Assistant",
        "firstMessage": "Hi! I'm your PropertyAI assistant. I can help you find properties in Mumbai, save your requirements, and book site visits. What are you looking for?",
        "model": {
            "provider": "google",
            "model": "gemini-2.0-flash",
            "temperature": 0.7,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are PropertyAI, a friendly and professional real estate voice assistant for properties in Mumbai, India. "
                        "Help users find properties by understanding their requirements: budget, location, BHK, property type. "
                        "Ask 1-2 questions at a time. Be conversational and natural. "
                        "Use the search_properties tool to find matching properties. "
                        "Use save_requirements to store their preferences. "
                        "Use book_visit to schedule property visits (ask for date and time). "
                        "Use save_contact to save their name and phone. "
                        "Always mention property names, prices, and locations clearly since this is a voice call. "
                        "Prices are in Indian Rupees — say amounts like '75 lakh' or '2.1 crore' instead of raw numbers. "
                        "Keep responses concise since this is a voice conversation."
                    ),
                }
            ],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "search_properties",
                        "description": "Search for properties matching user requirements",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "city": {"type": "string", "description": "City to search in, default Mumbai"},
                                "location": {"type": "string", "description": "Specific area or locality"},
                                "property_type": {"type": "string", "enum": ["apartment", "villa", "plot", "independent_house"]},
                                "bhk_min": {"type": "integer", "description": "Minimum BHK"},
                                "bhk_max": {"type": "integer", "description": "Maximum BHK"},
                                "budget_min": {"type": "number", "description": "Minimum budget in INR"},
                                "budget_max": {"type": "number", "description": "Maximum budget in INR"},
                            },
                            "required": ["city"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "save_requirements",
                        "description": "Save user's property requirements",
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
                            },
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "book_visit",
                        "description": "Book a property visit for the user",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "property_id": {"type": "integer", "description": "Property ID to visit"},
                                "visit_date": {"type": "string", "description": "Date in YYYY-MM-DD"},
                                "visit_time": {"type": "string", "description": "Time like 10:00 AM"},
                            },
                            "required": ["property_id", "visit_date", "visit_time"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "save_contact",
                        "description": "Save user's contact info (name, phone, email)",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "phone": {"type": "string"},
                                "email": {"type": "string"},
                            },
                            "required": ["name"],
                        },
                    },
                },
            ],
        },
        "voice": {
            "provider": "11labs",
            "voiceId": "21m00Tcm4TlvDq8ikWAM",  # Rachel - professional female voice
        },
        "serverUrl": f"{server_url}/api/vapi/webhook",
    }


@router.get("/assistant-config")
async def assistant_config(request: Request):
    """Return Vapi assistant config. Frontend uses this to start calls."""
    # Use PUBLIC_URL (ngrok) if set, otherwise fall back to request base URL
    server_url = settings.PUBLIC_URL or str(request.base_url).rstrip("/")
    config = get_assistant_config(server_url)
    return {
        "publicKey": settings.VAPI_PUBLIC_KEY,
        "assistantConfig": config,
    }
