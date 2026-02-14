"use client";

import { useEffect, useState } from "react";
import { fetchLeads } from "@/lib/api";
import { Lead } from "@/types";

const ADMIN_TOKEN = "admin-secret-change-me";

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);

  useEffect(() => {
    fetchLeads(ADMIN_TOKEN).then(setLeads).catch(() => {});
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-serif text-[#f0ebe4] mb-1 tracking-tight">Leads</h1>
      <p className="text-[#5a4a3a] text-sm mb-8 font-sans">All captured leads from sign-ups and conversations</p>

      {leads.length === 0 ? (
        <div className="bg-[#1a1714] border border-[#2e2a24] rounded-sm p-12 text-center">
          <p className="text-[#3a342c] font-sans">No leads yet. They appear when users sign up or chat.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {leads.map((lead) => (
            <div key={lead.id} className="bg-[#1a1714] border border-[#2e2a24] rounded-sm p-6 hover:border-[#c8a97e]/20 transition-colors duration-500">
              <div className="flex justify-between items-start">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 border border-[#c8a97e]/30 rounded-sm flex items-center justify-center">
                    <span className="text-sm font-serif text-[#c8a97e]">
                      {(lead.name || "?")[0].toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <h3 className="font-sans font-medium text-[#f0ebe4]">{lead.name || "Anonymous"}</h3>
                    <p className="text-sm text-[#5a4a3a] font-sans">
                      {lead.phone || "No phone"} &middot; {lead.email || "No email"}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <span className={`text-[10px] font-sans uppercase tracking-[0.15em] px-2.5 py-1 rounded-sm ${
                    lead.requirements.length > 0
                      ? "bg-[#7a9e6e]/10 text-[#7a9e6e] border border-[#7a9e6e]/20"
                      : "bg-[#c8a97e]/10 text-[#c8a97e] border border-[#c8a97e]/20"
                  }`}>
                    {lead.requirements.length > 0 ? "Qualified" : "New"}
                  </span>
                  <span className="text-xs text-[#3a342c] font-sans">{lead.created_at?.slice(0, 10)}</span>
                </div>
              </div>
              {lead.requirements.length > 0 && (
                <div className="mt-5 pt-4 border-t border-[#2e2a24]">
                  <p className="text-[10px] uppercase tracking-[0.2em] text-[#5a4a3a] font-sans font-medium mb-3">Requirements</p>
                  {lead.requirements.map((req, i) => (
                    <div key={i} className="flex flex-wrap gap-2 text-xs font-sans">
                      {req.city && <span className="bg-[#c8a97e]/8 text-[#c8a97e] px-2.5 py-1 rounded-sm border border-[#c8a97e]/15">City: {req.city}</span>}
                      {req.property_type && <span className="bg-[#c8a97e]/8 text-[#c8a97e] px-2.5 py-1 rounded-sm border border-[#c8a97e]/15 capitalize">Type: {req.property_type}</span>}
                      {req.budget_min && <span className="bg-[#7a9e6e]/8 text-[#7a9e6e] px-2.5 py-1 rounded-sm border border-[#7a9e6e]/15">Min: {req.budget_min.toLocaleString()}</span>}
                      {req.budget_max && <span className="bg-[#7a9e6e]/8 text-[#7a9e6e] px-2.5 py-1 rounded-sm border border-[#7a9e6e]/15">Max: {req.budget_max.toLocaleString()}</span>}
                      {req.bhk_min && <span className="bg-[#9e7ab3]/8 text-[#9e7ab3] px-2.5 py-1 rounded-sm border border-[#9e7ab3]/15">BHK: {req.bhk_min}{req.bhk_max ? `-${req.bhk_max}` : "+"}</span>}
                      {req.location_pref && <span className="bg-[#c8a97e]/8 text-[#c8a97e] px-2.5 py-1 rounded-sm border border-[#c8a97e]/15">Area: {req.location_pref}</span>}
                      {req.additional_notes && <span className="bg-[#f0ebe4]/5 text-[#8a8279] px-2.5 py-1 rounded-sm border border-[#2e2a24]">{req.additional_notes}</span>}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
