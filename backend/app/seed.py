import json
from app.database import SessionLocal, create_tables
from app.models import Property


SAMPLE_PROPERTIES = [
    {"title": "Sunshine 3BHK Apartment", "description": "Spacious 3BHK in a gated community with modern amenities.", "property_type": "apartment", "bhk": 3, "price": 8500000, "location": "Whitefield", "city": "Bangalore", "area_sqft": 1650, "amenities": json.dumps(["parking", "gym", "pool", "security", "garden"]), "image_url": None},
    {"title": "Green Valley 2BHK Flat", "description": "Affordable 2BHK near IT hub with excellent connectivity.", "property_type": "apartment", "bhk": 2, "price": 5500000, "location": "Electronic City", "city": "Bangalore", "area_sqft": 1100, "amenities": json.dumps(["parking", "security", "playground"]), "image_url": None},
    {"title": "Royal Orchid Villa", "description": "Luxurious 4BHK villa with private garden and pool.", "property_type": "villa", "bhk": 4, "price": 25000000, "location": "Sarjapur Road", "city": "Bangalore", "area_sqft": 3200, "amenities": json.dumps(["parking", "pool", "garden", "security", "clubhouse"]), "image_url": None},
    {"title": "Lake View 2BHK", "description": "Beautiful lake-facing apartment with serene views.", "property_type": "apartment", "bhk": 2, "price": 6200000, "location": "Hebbal", "city": "Bangalore", "area_sqft": 1200, "amenities": json.dumps(["parking", "gym", "security"]), "image_url": None},
    {"title": "Metro Heights 1BHK", "description": "Compact 1BHK ideal for young professionals, close to metro.", "property_type": "apartment", "bhk": 1, "price": 3200000, "location": "Marathahalli", "city": "Bangalore", "area_sqft": 650, "amenities": json.dumps(["parking", "security"]), "image_url": None},
    {"title": "Palm Residency 3BHK", "description": "Premium 3BHK with world-class amenities in prime location.", "property_type": "apartment", "bhk": 3, "price": 12000000, "location": "Bandra West", "city": "Mumbai", "area_sqft": 1400, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse"]), "image_url": None},
    {"title": "Sea Breeze 2BHK", "description": "Sea-facing 2BHK apartment with stunning ocean views.", "property_type": "apartment", "bhk": 2, "price": 18000000, "location": "Juhu", "city": "Mumbai", "area_sqft": 1100, "amenities": json.dumps(["parking", "gym", "security", "garden"]), "image_url": None},
    {"title": "Urban Nest 1BHK", "description": "Well-designed 1BHK in the heart of the city.", "property_type": "apartment", "bhk": 1, "price": 7500000, "location": "Andheri East", "city": "Mumbai", "area_sqft": 550, "amenities": json.dumps(["parking", "security"]), "image_url": None},
    {"title": "Heritage Villa", "description": "Elegant 5BHK independent villa with landscaped garden.", "property_type": "villa", "bhk": 5, "price": 45000000, "location": "Powai", "city": "Mumbai", "area_sqft": 4500, "amenities": json.dumps(["parking", "pool", "garden", "security", "gym", "clubhouse"]), "image_url": None},
    {"title": "Riverside Plot", "description": "Premium residential plot near the river with great appreciation potential.", "property_type": "plot", "bhk": None, "price": 8000000, "location": "Panvel", "city": "Mumbai", "area_sqft": 2400, "amenities": json.dumps([]), "image_url": None},
    {"title": "Garden City 3BHK", "description": "Spacious 3BHK in a well-maintained society.", "property_type": "apartment", "bhk": 3, "price": 7000000, "location": "Hinjewadi", "city": "Pune", "area_sqft": 1500, "amenities": json.dumps(["parking", "gym", "garden", "security", "playground"]), "image_url": None},
    {"title": "Skyline 2BHK", "description": "Modern 2BHK with rooftop access and city views.", "property_type": "apartment", "bhk": 2, "price": 4800000, "location": "Kharadi", "city": "Pune", "area_sqft": 1050, "amenities": json.dumps(["parking", "gym", "security"]), "image_url": None},
    {"title": "Woodland Villa", "description": "3BHK villa surrounded by greenery, perfect for families.", "property_type": "villa", "bhk": 3, "price": 15000000, "location": "Baner", "city": "Pune", "area_sqft": 2200, "amenities": json.dumps(["parking", "garden", "security", "clubhouse"]), "image_url": None},
    {"title": "Township Plot", "description": "Plot in upcoming township with all infrastructure planned.", "property_type": "plot", "bhk": None, "price": 3500000, "location": "Wagholi", "city": "Pune", "area_sqft": 1500, "amenities": json.dumps([]), "image_url": None},
    {"title": "Prestige Tower 4BHK", "description": "Ultra-premium 4BHK penthouse with panoramic views.", "property_type": "apartment", "bhk": 4, "price": 35000000, "location": "Koregaon Park", "city": "Pune", "area_sqft": 2800, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse", "concierge"]), "image_url": None},
    {"title": "DLF 3BHK Apartment", "description": "Well-designed 3BHK in DLF township with great connectivity.", "property_type": "apartment", "bhk": 3, "price": 9500000, "location": "Gurgaon Sector 42", "city": "Delhi NCR", "area_sqft": 1700, "amenities": json.dumps(["parking", "gym", "pool", "security", "garden"]), "image_url": None},
    {"title": "Noida 2BHK Smart Home", "description": "Tech-enabled 2BHK with smart home features.", "property_type": "apartment", "bhk": 2, "price": 5000000, "location": "Noida Sector 75", "city": "Delhi NCR", "area_sqft": 1050, "amenities": json.dumps(["parking", "gym", "security", "smart_home"]), "image_url": None},
    {"title": "Farmhouse Estate", "description": "Expansive farmhouse with 1 acre of land.", "property_type": "independent_house", "bhk": 6, "price": 80000000, "location": "Chattarpur", "city": "Delhi NCR", "area_sqft": 8000, "amenities": json.dumps(["parking", "pool", "garden", "security"]), "image_url": None},
    {"title": "Marina Bay 2BHK", "description": "Waterfront 2BHK with modern interiors and bay views.", "property_type": "apartment", "bhk": 2, "price": 6800000, "location": "OMR", "city": "Chennai", "area_sqft": 1150, "amenities": json.dumps(["parking", "gym", "pool", "security"]), "image_url": None},
    {"title": "Temple Town Villa", "description": "Traditional-style 3BHK independent house.", "property_type": "independent_house", "bhk": 3, "price": 9000000, "location": "Adyar", "city": "Chennai", "area_sqft": 1800, "amenities": json.dumps(["parking", "garden"]), "image_url": None},
]


def seed_database():
    create_tables()
    db = SessionLocal()
    try:
        existing = db.query(Property).count()
        if existing > 0:
            print(f"Database already has {existing} properties. Skipping seed.")
            return

        for data in SAMPLE_PROPERTIES:
            prop = Property(**data)
            db.add(prop)

        db.commit()
        print(f"Seeded {len(SAMPLE_PROPERTIES)} properties successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
