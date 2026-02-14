export interface Property {
  id: number;
  title: string;
  description: string | null;
  property_type: string;
  bhk: number | null;
  price: number;
  location: string;
  city: string;
  area_sqft: number | null;
  amenities: string | null;
  status: string;
  image_url: string | null;
}

export interface ChatMessage {
  role: "user" | "agent";
  text: string;
  properties?: Property[];
  booking?: BookingConfirmation;
}

export interface BookingConfirmation {
  success: boolean;
  booking_id: number;
  property_title: string;
  visit_date: string;
  visit_time: string;
}

export interface Booking {
  id: number;
  lead_name: string;
  lead_phone: string;
  property_title: string;
  property_id: number;
  visit_date: string;
  visit_time: string;
  status: string;
  created_at: string;
}

export interface Lead {
  id: number;
  session_id: string;
  name: string | null;
  phone: string | null;
  email: string | null;
  created_at: string;
  requirements: Requirement[];
}

export interface Requirement {
  budget_min: number | null;
  budget_max: number | null;
  city: string | null;
  location_pref: string | null;
  property_type: string | null;
  bhk_min: number | null;
  bhk_max: number | null;
  amenities: string | null;
  additional_notes: string | null;
}
