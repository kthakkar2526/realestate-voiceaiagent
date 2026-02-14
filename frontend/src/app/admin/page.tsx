"use client";

import { useEffect, useState } from "react";
import { fetchProperties, fetchBookings, fetchLeads } from "@/lib/api";
import { Booking, Lead } from "@/types";

const ADMIN_TOKEN = "admin-secret-change-me";

export default function AdminDashboard() {
  const [stats, setStats] = useState({ properties: 0, bookings: 0, leads: 0 });
  const [recentBookings, setRecentBookings] = useState<Booking[]>([]);
  const [recentLeads, setRecentLeads] = useState<Lead[]>([]);

  useEffect(() => {
    Promise.all([
      fetchProperties().then((d) => d.length),
      fetchBookings(ADMIN_TOKEN).then((d: Booking[]) => {
        setRecentBookings(d.slice(0, 5));
        return d.length;
      }).catch(() => 0),
      fetchLeads(ADMIN_TOKEN).then((d: Lead[]) => {
        setRecentLeads(d.slice(0, 5));
        return d.length;
      }).catch(() => 0),
    ]).then(([properties, bookings, leads]) => {
      setStats({ properties, bookings, leads });
    });
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-serif text-[#f0ebe4] mb-1 tracking-tight">Dashboard</h1>
      <p className="text-[#5a4a3a] text-sm font-sans mb-10">Overview of your PropertyAI system</p>

      {/* Stats Cards */}
      <div className="grid grid-cols-3 gap-6 mb-12">
        <div className="bg-[#1a1714] border border-[#2e2a24] rounded-sm p-6 hover:border-[#c8a97e]/20 transition-colors duration-500">
          <div className="flex items-center justify-between">
            <p className="text-xs text-[#5a4a3a] font-sans uppercase tracking-[0.15em]">Properties</p>
            <div className="w-10 h-10 border border-[#c8a97e]/20 rounded-sm flex items-center justify-center">
              <svg className="w-5 h-5 text-[#c8a97e]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
          </div>
          <p className="text-3xl font-serif text-[#f0ebe4] mt-4 tracking-tight">{stats.properties}</p>
          <p className="text-xs text-[#3a342c] mt-1 font-sans">Active listings</p>
        </div>
        <div className="bg-[#1a1714] border border-[#2e2a24] rounded-sm p-6 hover:border-[#c8a97e]/20 transition-colors duration-500">
          <div className="flex items-center justify-between">
            <p className="text-xs text-[#5a4a3a] font-sans uppercase tracking-[0.15em]">Bookings</p>
            <div className="w-10 h-10 border border-[#7a9e6e]/20 rounded-sm flex items-center justify-center">
              <svg className="w-5 h-5 text-[#7a9e6e]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <p className="text-3xl font-serif text-[#f0ebe4] mt-4 tracking-tight">{stats.bookings}</p>
          <p className="text-xs text-[#3a342c] mt-1 font-sans">Visit requests</p>
        </div>
        <div className="bg-[#1a1714] border border-[#2e2a24] rounded-sm p-6 hover:border-[#c8a97e]/20 transition-colors duration-500">
          <div className="flex items-center justify-between">
            <p className="text-xs text-[#5a4a3a] font-sans uppercase tracking-[0.15em]">Leads</p>
            <div className="w-10 h-10 border border-[#9e7ab3]/20 rounded-sm flex items-center justify-center">
              <svg className="w-5 h-5 text-[#9e7ab3]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
          </div>
          <p className="text-3xl font-serif text-[#f0ebe4] mt-4 tracking-tight">{stats.leads}</p>
          <p className="text-xs text-[#3a342c] mt-1 font-sans">Captured leads</p>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Recent Leads */}
        <div className="bg-[#1a1714] border border-[#2e2a24] rounded-sm p-6">
          <h3 className="font-serif text-[#f0ebe4] mb-5 tracking-tight">Recent Leads</h3>
          {recentLeads.length === 0 ? (
            <p className="text-sm text-[#3a342c] font-sans">No leads yet</p>
          ) : (
            <div className="space-y-0">
              {recentLeads.map((lead) => (
                <div key={lead.id} className="flex items-center justify-between py-3 border-b border-[#2e2a24] last:border-0">
                  <div>
                    <p className="text-sm font-sans font-medium text-[#f0ebe4]">{lead.name || "Anonymous"}</p>
                    <p className="text-xs text-[#5a4a3a] font-sans">{lead.phone || lead.email || "No contact"}</p>
                  </div>
                  <div className="text-right">
                    <span className={`text-[10px] font-sans uppercase tracking-[0.15em] px-2.5 py-1 rounded-sm ${
                      lead.requirements.length > 0
                        ? "bg-[#7a9e6e]/10 text-[#7a9e6e] border border-[#7a9e6e]/20"
                        : "bg-[#c8a97e]/10 text-[#c8a97e] border border-[#c8a97e]/20"
                    }`}>
                      {lead.requirements.length > 0 ? "Qualified" : "New"}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Bookings */}
        <div className="bg-[#1a1714] border border-[#2e2a24] rounded-sm p-6">
          <h3 className="font-serif text-[#f0ebe4] mb-5 tracking-tight">Recent Bookings</h3>
          {recentBookings.length === 0 ? (
            <p className="text-sm text-[#3a342c] font-sans">No bookings yet</p>
          ) : (
            <div className="space-y-0">
              {recentBookings.map((b) => (
                <div key={b.id} className="flex items-center justify-between py-3 border-b border-[#2e2a24] last:border-0">
                  <div>
                    <p className="text-sm font-sans font-medium text-[#f0ebe4]">{b.property_title}</p>
                    <p className="text-xs text-[#5a4a3a] font-sans">{b.lead_name || "Unknown"} &middot; {b.visit_date}</p>
                  </div>
                  <span className={`text-[10px] font-sans uppercase tracking-[0.15em] px-2.5 py-1 rounded-sm ${
                    b.status === "confirmed" ? "bg-[#7a9e6e]/10 text-[#7a9e6e] border border-[#7a9e6e]/20" :
                    b.status === "cancelled" ? "bg-[#d4836a]/10 text-[#d4836a] border border-[#d4836a]/20" :
                    "bg-[#c8a97e]/10 text-[#c8a97e] border border-[#c8a97e]/20"
                  }`}>
                    {b.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
