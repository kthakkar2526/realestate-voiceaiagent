const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function sendMessage(sessionId: string, message: string, token?: string | null) {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers,
    body: JSON.stringify({ session_id: sessionId, message }),
  });
  if (!res.ok) throw new Error("Chat request failed");
  return res.json();
}

export async function fetchProperties(params?: Record<string, string>) {
  const query = params ? "?" + new URLSearchParams(params).toString() : "";
  const res = await fetch(`${API_BASE}/api/properties${query}`);
  if (!res.ok) throw new Error("Failed to fetch properties");
  return res.json();
}

export async function fetchBookings(token: string) {
  const res = await fetch(`${API_BASE}/api/bookings`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch bookings");
  return res.json();
}

export async function updateBooking(token: string, id: number, status: string) {
  const res = await fetch(`${API_BASE}/api/bookings/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) throw new Error("Failed to update booking");
  return res.json();
}

export async function fetchLeads(token: string) {
  const res = await fetch(`${API_BASE}/api/leads`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch leads");
  return res.json();
}

export async function createProperty(token: string, data: Record<string, unknown>) {
  const res = await fetch(`${API_BASE}/api/properties`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create property");
  return res.json();
}

export async function deleteProperty(token: string, id: number) {
  const res = await fetch(`${API_BASE}/api/properties/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to delete property");
  return res.json();
}
