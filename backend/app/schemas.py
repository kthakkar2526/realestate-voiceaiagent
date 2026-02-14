from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    message: str
    properties: list[dict] | None = None
    booking: dict | None = None


class PropertyCreate(BaseModel):
    title: str
    description: str | None = None
    property_type: str
    bhk: int | None = None
    price: float
    location: str
    city: str
    area_sqft: float | None = None
    amenities: str | None = None
    status: str = "available"
    image_url: str | None = None


class PropertyUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    property_type: str | None = None
    bhk: int | None = None
    price: float | None = None
    location: str | None = None
    city: str | None = None
    area_sqft: float | None = None
    amenities: str | None = None
    status: str | None = None
    image_url: str | None = None


class BookingUpdate(BaseModel):
    status: str
