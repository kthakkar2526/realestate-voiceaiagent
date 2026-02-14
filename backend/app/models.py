from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20), unique=True, nullable=False)
    name = Column(String(255))
    email = Column(String(255))
    otp_code = Column(String(6))
    otp_expires_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    leads = relationship("Lead", back_populates="user")


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    property_type = Column(String(50), nullable=False)  # apartment, villa, plot, independent_house
    bhk = Column(Integer)
    price = Column(Float, nullable=False)
    location = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    area_sqft = Column(Float)
    amenities = Column(Text)  # JSON array as text
    status = Column(String(20), nullable=False, default="available")
    image_url = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    bookings = relationship("Booking", back_populates="property")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "property_type": self.property_type,
            "bhk": self.bhk,
            "price": self.price,
            "location": self.location,
            "city": self.city,
            "area_sqft": self.area_sqft,
            "amenities": self.amenities,
            "status": self.status,
            "image_url": self.image_url,
        }


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    last_activity_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="leads")
    requirements = relationship("Requirement", back_populates="lead")
    bookings = relationship("Booking", back_populates="lead")


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    budget_min = Column(Float)
    budget_max = Column(Float)
    location_pref = Column(String(255))
    city = Column(String(100))
    property_type = Column(String(50))
    bhk_min = Column(Integer)
    bhk_max = Column(Integer)
    amenities = Column(Text)
    additional_notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    lead = relationship("Lead", back_populates="requirements")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    visit_date = Column(String(20), nullable=False)
    visit_time = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    notes = Column(Text)
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    lead = relationship("Lead", back_populates="bookings")
    property = relationship("Property", back_populates="bookings")
