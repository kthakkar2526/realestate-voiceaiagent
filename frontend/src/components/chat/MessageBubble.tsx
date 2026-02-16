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
              ? "bg-[#c8a97e] text-white rounded-br-none"
              : "bg-white border border-[#e0d9cf] text-[#1a1714] rounded-bl-none"
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
          <div className="mt-2 bg-[#e8f5e2] border border-[#c5e1b8] rounded-sm p-3.5 text-sm font-sans">
            <p className="font-medium text-[#4a7c3f]">Visit Booked</p>
            <p className="text-[#5a8c4e] mt-0.5">{message.booking.property_title}</p>
            <p className="text-[#4a7c3f]/70 text-xs mt-1">
              {message.booking.visit_date} at {message.booking.visit_time}
            </p>
            <p className="text-xs text-[#8a8279] mt-1.5">
              Booking #{message.booking.booking_id}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
