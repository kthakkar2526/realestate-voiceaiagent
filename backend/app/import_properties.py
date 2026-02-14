"""
Import real/realistic property data into the database.

Usage:
    # With Apify (requires APIFY_TOKEN in .env):
    python -m app.import_properties --source apify --city Mumbai

    # With realistic curated data (no API needed):
    python -m app.import_properties --source curated
"""

import json
import argparse
import requests
from app.database import SessionLocal, create_tables
from app.models import Property, Booking
from app.config import settings

# ---------------------------------------------------------------------------
# Apify-based import (99acres scraper)
# ---------------------------------------------------------------------------

APIFY_ACTOR_ID = "fatihtahta~99acres-scraper-ppe"  # 99acres scraper on Apify

def fetch_from_apify(city: str = "Mumbai", max_items: int = 30) -> list[dict]:
    """Run 99acres Apify actor and return property data."""
    token = getattr(settings, "APIFY_TOKEN", "") or ""
    if not token:
        print("[ERROR] APIFY_TOKEN not set in .env. Use --source curated instead.")
        return []

    print(f"[APIFY] Starting 99acres scraper for {city}...")
    run_url = f"https://api.apify.com/v2/acts/{APIFY_ACTOR_ID}/runs"
    run_input = {
        "Locations": [city],
        "maxItems": max_items,
    }

    resp = requests.post(
        run_url,
        json=run_input,
        params={"token": token},
        timeout=30,
    )
    if resp.status_code != 201:
        print(f"[ERROR] Failed to start Apify run: {resp.status_code} {resp.text}")
        return []

    run_data = resp.json()["data"]
    run_id = run_data["id"]
    print(f"[APIFY] Run started: {run_id}. Waiting for results...")

    # Wait for run to finish
    import time
    for _ in range(60):  # max 5 min
        time.sleep(5)
        status_resp = requests.get(
            f"https://api.apify.com/v2/actor-runs/{run_id}",
            params={"token": token},
            timeout=15,
        )
        run_info = status_resp.json()["data"]
        status = run_info["status"]
        if status == "SUCCEEDED":
            break
        elif status in ("FAILED", "ABORTED", "TIMED-OUT"):
            print(f"[ERROR] Apify run {status}")
            # Print error details
            status_msg = run_info.get("statusMessage", "")
            if status_msg:
                print(f"[ERROR] Message: {status_msg}")
            # Try to get log
            log_resp = requests.get(
                f"https://api.apify.com/v2/actor-runs/{run_id}/log",
                params={"token": token},
                timeout=15,
            )
            if log_resp.ok:
                log_text = log_resp.text[-1000:]  # last 1000 chars
                print(f"[LOG] {log_text}")
            return []
        print(f"  ... status: {status}")

    # Fetch dataset items
    dataset_id = run_data["defaultDatasetId"]
    items_resp = requests.get(
        f"https://api.apify.com/v2/datasets/{dataset_id}/items",
        params={"token": token, "format": "json"},
        timeout=30,
    )
    raw_items = items_resp.json()
    print(f"[APIFY] Got {len(raw_items)} items from 99acres")

    # Debug: print first item's keys
    if raw_items:
        print(f"[DEBUG] Sample item keys: {list(raw_items[0].keys())}")
        import pprint
        pprint.pprint(raw_items[0])

    # Map Apify output to our Property schema
    properties = []
    for item in raw_items:
        try:
            prop = map_apify_item(item, city)
            if prop:
                properties.append(prop)
        except Exception as e:
            print(f"  Skipping item: {e}")
    return properties


def map_apify_item(item: dict, default_city: str) -> dict | None:
    """Map a 99acres Apify item to our Property fields."""
    title = item.get("title") or item.get("name") or ""
    if not title:
        return None

    price = item.get("price") or item.get("price_numeric") or 0
    if isinstance(price, str):
        price = parse_price_string(price)
    if not price or price <= 0:
        return None

    # Determine BHK
    bhk = item.get("bhk") or item.get("bedrooms")
    if isinstance(bhk, str):
        import re
        match = re.search(r"(\d+)", bhk)
        bhk = int(match.group(1)) if match else None

    # Property type
    ptype = item.get("property_type", "apartment").lower()
    if "villa" in ptype:
        ptype = "villa"
    elif "plot" in ptype or "land" in ptype:
        ptype = "plot"
    elif "house" in ptype or "independent" in ptype:
        ptype = "independent_house"
    else:
        ptype = "apartment"

    area = item.get("area_sqft") or item.get("carpet_area") or item.get("super_area") or 0
    if isinstance(area, str):
        import re
        match = re.search(r"([\d,.]+)", area)
        area = float(match.group(1).replace(",", "")) if match else 0

    location = item.get("locality") or item.get("location") or item.get("address") or ""
    city = item.get("city") or default_city

    amenities_list = item.get("amenities") or []
    if isinstance(amenities_list, str):
        amenities_list = [a.strip() for a in amenities_list.split(",")]

    return {
        "title": title[:255],
        "description": item.get("description", "")[:1000] or f"{bhk or ''}BHK {ptype} in {location}, {city}",
        "property_type": ptype,
        "bhk": int(bhk) if bhk else None,
        "price": float(price),
        "location": location[:255] or city,
        "city": city[:100],
        "area_sqft": float(area) if area else None,
        "amenities": json.dumps(amenities_list[:10]),
        "image_url": item.get("image") or item.get("imageUrl") or None,
    }


def parse_price_string(price_str: str) -> float:
    """Parse Indian price strings like '1.2 Cr', '45 Lac' etc."""
    import re
    price_str = price_str.replace(",", "").replace("₹", "").strip()
    match = re.search(r"([\d.]+)\s*(cr|crore|Cr)", price_str, re.IGNORECASE)
    if match:
        return float(match.group(1)) * 10_000_000
    match = re.search(r"([\d.]+)\s*(lac|lakh|Lac|L)", price_str, re.IGNORECASE)
    if match:
        return float(match.group(1)) * 100_000
    match = re.search(r"([\d.]+)", price_str)
    if match:
        return float(match.group(1))
    return 0


# ---------------------------------------------------------------------------
# Curated realistic Mumbai data (no API needed)
# ---------------------------------------------------------------------------

MUMBAI_PROPERTIES = [
    {"title": "Lodha Palava 2BHK", "description": "Spacious 2BHK in Lodha Palava township with world-class amenities. Close to upcoming metro station and Palava city center.", "property_type": "apartment", "bhk": 2, "price": 7500000, "location": "Dombivli East", "city": "Mumbai", "area_sqft": 950, "amenities": json.dumps(["parking", "gym", "pool", "security", "garden", "clubhouse", "playground"]), "image_url": None},
    {"title": "Oberoi Realty Sky City 3BHK", "description": "Premium 3BHK in Oberoi Sky City with panoramic views of Thane creek. Italian marble flooring, modular kitchen.", "property_type": "apartment", "bhk": 3, "price": 21000000, "location": "Borivali East", "city": "Mumbai", "area_sqft": 1350, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse", "concierge", "garden"]), "image_url": None},
    {"title": "Hiranandani Fortune City 2BHK", "description": "Well-designed 2BHK in Hiranandani Fortune City. Vastu-compliant, cross-ventilation, modular kitchen.", "property_type": "apartment", "bhk": 2, "price": 8900000, "location": "Panvel", "city": "Mumbai", "area_sqft": 1050, "amenities": json.dumps(["parking", "gym", "pool", "security", "garden", "jogging_track"]), "image_url": None},
    {"title": "Godrej Platinum 4BHK", "description": "Ultra-luxury 4BHK in Godrej Platinum, Vikhroli. Floor-to-ceiling windows, private lift lobby, designer fittings.", "property_type": "apartment", "bhk": 4, "price": 65000000, "location": "Vikhroli East", "city": "Mumbai", "area_sqft": 2800, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse", "concierge", "spa", "theater"]), "image_url": None},
    {"title": "Rustomjee Crown 3BHK", "description": "Sea-facing 3BHK in Rustomjee Crown, Prabhadevi. Walking distance to Siddhivinayak Temple and Dadar station.", "property_type": "apartment", "bhk": 3, "price": 45000000, "location": "Prabhadevi", "city": "Mumbai", "area_sqft": 1600, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse", "garden"]), "image_url": None},
    {"title": "Runwal Forests 1BHK", "description": "Affordable 1BHK in Runwal Forests surrounded by 5 acres of forest land. Perfect for first-time buyers.", "property_type": "apartment", "bhk": 1, "price": 4500000, "location": "Kanjurmarg West", "city": "Mumbai", "area_sqft": 550, "amenities": json.dumps(["parking", "security", "garden", "jogging_track"]), "image_url": None},
    {"title": "Raheja Vivarea 3BHK", "description": "Iconic sea-view 3BHK at Raheja Vivarea, Jacob Circle. One of Mumbai's most prestigious addresses.", "property_type": "apartment", "bhk": 3, "price": 72000000, "location": "Mahalaxmi", "city": "Mumbai", "area_sqft": 2100, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse", "concierge", "spa"]), "image_url": None},
    {"title": "Dosti West County 2BHK", "description": "Value-for-money 2BHK in Dosti West County. 10 mins from Balkum station, surrounded by greenery.", "property_type": "apartment", "bhk": 2, "price": 6200000, "location": "Balkum, Thane", "city": "Mumbai", "area_sqft": 850, "amenities": json.dumps(["parking", "gym", "pool", "security", "playground"]), "image_url": None},
    {"title": "Indiabulls Blu 2BHK", "description": "Modern 2BHK in Indiabulls Blu with stunning Worli sea-link views. Smart home enabled.", "property_type": "apartment", "bhk": 2, "price": 35000000, "location": "Worli", "city": "Mumbai", "area_sqft": 1100, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse", "smart_home"]), "image_url": None},
    {"title": "Puraniks Rumah Bali 2BHK", "description": "Bali-themed 2BHK apartment with exotic landscaping. Close to Ghodbunder road.", "property_type": "apartment", "bhk": 2, "price": 7800000, "location": "Thane West", "city": "Mumbai", "area_sqft": 950, "amenities": json.dumps(["parking", "gym", "pool", "security", "garden", "clubhouse"]), "image_url": None},
    {"title": "Shapoorji Pallonji Joyville 3BHK", "description": "Family-friendly 3BHK with dedicated kids' zones and senior citizen areas. Near Virar station.", "property_type": "apartment", "bhk": 3, "price": 5800000, "location": "Virar West", "city": "Mumbai", "area_sqft": 1200, "amenities": json.dumps(["parking", "gym", "pool", "security", "playground", "garden"]), "image_url": None},
    {"title": "Kanakia Rainforest 2BHK", "description": "Nature-inspired 2BHK in Kanakia Rainforest. Built around 1.5 lakh sqft of forest area.", "property_type": "apartment", "bhk": 2, "price": 11500000, "location": "Andheri East", "city": "Mumbai", "area_sqft": 1000, "amenities": json.dumps(["parking", "gym", "pool", "security", "garden", "jogging_track", "clubhouse"]), "image_url": None},
    {"title": "Wadhwa The Address 1BHK", "description": "Compact luxury 1BHK at Wadhwa The Address. Walking distance to Ghatkopar metro station.", "property_type": "apartment", "bhk": 1, "price": 9500000, "location": "Ghatkopar West", "city": "Mumbai", "area_sqft": 650, "amenities": json.dumps(["parking", "gym", "security", "clubhouse"]), "image_url": None},
    {"title": "Marathon Monte South 3BHK", "description": "Premium 3BHK at Monte South, Byculla. Heritage neighbourhood, modern luxury living.", "property_type": "apartment", "bhk": 3, "price": 38000000, "location": "Byculla", "city": "Mumbai", "area_sqft": 1450, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse", "garden", "theater"]), "image_url": None},
    {"title": "Independent House Goregaon", "description": "3BHK independent house with private terrace and parking. Quiet lane in Goregaon West.", "property_type": "independent_house", "bhk": 3, "price": 28000000, "location": "Goregaon West", "city": "Mumbai", "area_sqft": 1800, "amenities": json.dumps(["parking", "garden", "terrace"]), "image_url": None},
    {"title": "Lodha Amara 1BHK", "description": "Smart 1BHK in Lodha Amara, Kolshet Road. Ideal investment with high rental yield in Thane.", "property_type": "apartment", "bhk": 1, "price": 5200000, "location": "Kolshet, Thane", "city": "Mumbai", "area_sqft": 580, "amenities": json.dumps(["parking", "gym", "pool", "security"]), "image_url": None},
    {"title": "Piramal Mahalaxmi 2BHK", "description": "South Mumbai luxury 2BHK with views of the racecourse. Piramal's flagship project.", "property_type": "apartment", "bhk": 2, "price": 42000000, "location": "Mahalaxmi", "city": "Mumbai", "area_sqft": 1250, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse", "concierge", "spa"]), "image_url": None},
    {"title": "Tata Serein 2BHK", "description": "Tata-quality 2BHK in Serein, Pokhran Road. Walking distance to Viviana Mall and Jupiter Hospital.", "property_type": "apartment", "bhk": 2, "price": 10500000, "location": "Pokhran Road, Thane", "city": "Mumbai", "area_sqft": 1000, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse", "garden"]), "image_url": None},
    {"title": "Residential Plot Karjat", "description": "1200 sqft NA plot in upcoming Karjat area. Mountain views, perfect for weekend home.", "property_type": "plot", "bhk": None, "price": 1800000, "location": "Karjat", "city": "Mumbai", "area_sqft": 1200, "amenities": json.dumps([]), "image_url": None},
    {"title": "Birla Vanya 3BHK Villa", "description": "Luxury 3BHK villa in Birla Vanya township. 15 mins from Kalyan station, surrounded by hills.", "property_type": "villa", "bhk": 3, "price": 16000000, "location": "Kalyan West", "city": "Mumbai", "area_sqft": 2200, "amenities": json.dumps(["parking", "gym", "pool", "security", "garden", "clubhouse", "jogging_track"]), "image_url": None},
    {"title": "Sunteck City Avenue 2BHK", "description": "Affordable luxury 2BHK at Sunteck City. Direct connectivity to Western Express Highway.", "property_type": "apartment", "bhk": 2, "price": 8500000, "location": "Goregaon West", "city": "Mumbai", "area_sqft": 900, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse"]), "image_url": None},
    {"title": "Ariisto Sommet 4BHK", "description": "Exclusive 4BHK penthouse in Ariisto Sommet. Double-height living room, private terrace pool.", "property_type": "apartment", "bhk": 4, "price": 55000000, "location": "Goregaon East", "city": "Mumbai", "area_sqft": 3000, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse", "concierge", "terrace"]), "image_url": None},
    {"title": "Mahindra Alcove 2BHK", "description": "Thoughtfully designed 2BHK in Mahindra Alcove, Chandivali. Near Powai lake and JVLR.", "property_type": "apartment", "bhk": 2, "price": 13500000, "location": "Chandivali", "city": "Mumbai", "area_sqft": 1050, "amenities": json.dumps(["parking", "gym", "pool", "security", "garden"]), "image_url": None},
    {"title": "Raymond Realty Ten X Habitat 1BHK", "description": "Raymond's first real estate project. Smart 1BHK with premium finishes in Thane.", "property_type": "apartment", "bhk": 1, "price": 4800000, "location": "Pokhran Road, Thane", "city": "Mumbai", "area_sqft": 540, "amenities": json.dumps(["parking", "gym", "pool", "security", "garden"]), "image_url": None},
    {"title": "Hubtown Sunstone 3BHK", "description": "Well-connected 3BHK near Bandra-Kurla Complex. Premium business district location.", "property_type": "apartment", "bhk": 3, "price": 32000000, "location": "Bandra East", "city": "Mumbai", "area_sqft": 1350, "amenities": json.dumps(["parking", "gym", "pool", "security", "clubhouse"]), "image_url": None},
]


# ---------------------------------------------------------------------------
# Import logic
# ---------------------------------------------------------------------------

def import_properties(properties: list[dict], replace: bool = False):
    """Insert properties into database."""
    create_tables()
    db = SessionLocal()
    try:
        if replace:
            bookings_deleted = db.query(Booking).delete()
            if bookings_deleted:
                print(f"Cleared {bookings_deleted} existing bookings.")
            deleted = db.query(Property).delete()
            print(f"Cleared {deleted} existing properties.")

        count = 0
        for data in properties:
            data["status"] = "available"
            prop = Property(**data)
            db.add(prop)
            count += 1

        db.commit()
        print(f"Imported {count} properties successfully.")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Import property data")
    parser.add_argument("--source", choices=["apify", "curated"], default="curated",
                        help="Data source: apify (99acres scraper) or curated (realistic Mumbai data)")
    parser.add_argument("--city", default="Mumbai", help="City for Apify search")
    parser.add_argument("--max-items", type=int, default=30, help="Max items from Apify")
    parser.add_argument("--replace", action="store_true", help="Replace existing properties")
    args = parser.parse_args()

    if args.source == "apify":
        properties = fetch_from_apify(args.city, args.max_items)
        if not properties:
            print("No properties from Apify. Falling back to curated data.")
            properties = MUMBAI_PROPERTIES
    else:
        properties = MUMBAI_PROPERTIES

    import_properties(properties, replace=args.replace)


if __name__ == "__main__":
    main()
