"use client";

import { useEffect, useState } from "react";
import { fetchBookings, updateBooking } from "@/lib/api";
import { Booking } from "@/types";

const ADMIN_TOKEN = "admin-secret-change-me";

export default function BookingsPage() {
  const [bookings, setBookings] = useState<Booking[]>([]);

  const load = () => fetchBookings(ADMIN_TOKEN).then(setBookings).catch(() => {});
  useEffect(() => { load(); }, []);

  const handleStatus = async (id: number, status: string) => {
    await updateBooking(ADMIN_TOKEN, id, status);
    load();
  };

  return (
    <div>
      <h1 className="text-2xl font-serif text-[#f0ebe4] mb-1 tracking-tight">Bookings</h1>
      <p className="text-[#5a4a3a] text-sm mb-8 font-sans">Manage property visit requests</p>

      {bookings.length === 0 ? (
        <div className="bg-[#1a1714] border border-[#2e2a24] rounded-sm p-12 text-center">
          <p className="text-[#3a342c] font-sans">No bookings yet. They appear when users book visits through the chat.</p>
        </div>
      ) : (
        <div className="bg-[#1a1714] border border-[#2e2a24] rounded-sm overflow-hidden">
          <table className="w-full text-sm font-sans">
            <thead className="border-b border-[#2e2a24] text-left">
              <tr>
                <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">ID</th>
                <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Lead</th>
                <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Phone</th>
                <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Property</th>
                <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Date</th>
                <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Time</th>
                <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Status</th>
                <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2e2a24]/50">
              {bookings.map((b) => (
                <tr key={b.id} className="hover:bg-[#f0ebe4]/2 transition-colors duration-300">
                  <td className="px-5 py-3.5 text-[#5a4a3a]">#{b.id}</td>
                  <td className="px-5 py-3.5 font-medium text-[#f0ebe4]">{b.lead_name || "Unknown"}</td>
                  <td className="px-5 py-3.5 text-[#8a8279]">{b.lead_phone || "-"}</td>
                  <td className="px-5 py-3.5 text-[#f0ebe4]/80">{b.property_title}</td>
                  <td className="px-5 py-3.5 text-[#8a8279]">{b.visit_date}</td>
                  <td className="px-5 py-3.5 text-[#8a8279]">{b.visit_time}</td>
                  <td className="px-5 py-3.5">
                    <span className={`text-[10px] uppercase tracking-[0.15em] px-2.5 py-1 rounded-sm font-sans ${
                      b.status === "confirmed" ? "bg-[#7a9e6e]/10 text-[#7a9e6e] border border-[#7a9e6e]/20" :
                      b.status === "cancelled" ? "bg-[#d4836a]/10 text-[#d4836a] border border-[#d4836a]/20" :
                      "bg-[#c8a97e]/10 text-[#c8a97e] border border-[#c8a97e]/20"
                    }`}>
                      {b.status}
                    </span>
                  </td>
                  <td className="px-5 py-3.5">
                    {b.status === "pending" && (
                      <div className="flex gap-3">
                        <button onClick={() => handleStatus(b.id, "confirmed")} className="text-[#7a9e6e] hover:text-[#8fb87e] text-xs font-medium font-sans transition-colors duration-300">Confirm</button>
                        <button onClick={() => handleStatus(b.id, "cancelled")} className="text-[#d4836a] hover:text-[#e09480] text-xs font-medium font-sans transition-colors duration-300">Cancel</button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
