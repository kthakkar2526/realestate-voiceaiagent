"use client";

import { ChatMessage } from "@/types";
import PropertyCard from "./PropertyCard";

export default function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
      <div className={`max-w-[80%] ${isUser ? "order-2" : "order-1"}`}>
        <div
          className={`px-4 py-3 rounded-sm text-sm leading-relaxed font-sans ${
            isUser
              ? "bg-[#c8a97e] text-[#13110e] rounded-br-none"
              : "bg-[#1a1714] border border-[#2e2a24] text-[#f0ebe4] rounded-bl-none"
          }`}
        >
          <p className="whitespace-pre-wrap">{message.text}</p>
        </div>
        {message.properties && message.properties.length > 0 && (
          <div className="mt-2 space-y-2">
            {message.properties.map((p) => (
              <PropertyCard key={p.id} property={p} />
            ))}
          </div>
        )}
        {message.booking && message.booking.success && (
          <div className="mt-2 bg-[#7a9e6e]/10 border border-[#7a9e6e]/20 rounded-sm p-3.5 text-sm font-sans">
            <p className="font-medium text-[#7a9e6e]">Visit Booked</p>
            <p className="text-[#8fb87e] mt-0.5">{message.booking.property_title}</p>
            <p className="text-[#7a9e6e]/70 text-xs mt-1">
              {message.booking.visit_date} at {message.booking.visit_time}
            </p>
            <p className="text-xs text-[#5a4a3a] mt-1.5">
              Booking #{message.booking.booking_id}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
