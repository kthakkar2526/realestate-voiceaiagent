"use client";

import { useState, useRef, useEffect } from "react";
import { ChatMessage } from "@/types";
import { sendMessage } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import MessageBubble from "./MessageBubble";

function getSessionId(): string {
  if (typeof window === "undefined") return "";
  let id = localStorage.getItem("re_session_id");
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem("re_session_id", id);
  }
  return id;
}

export default function ChatWindow() {
  const { token } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    setMessages([
      {
        role: "agent",
        text: "Hello! I'm your real estate assistant. I can help you find the perfect property and book visits. What are you looking for today?",
      },
    ]);
  }, []);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", text }]);
    setLoading(true);

    try {
      const data = await sendMessage(getSessionId(), text, token);
      const agentMsg: ChatMessage = {
        role: "agent",
        text: data.message,
        properties: data.properties || undefined,
        booking: data.booking || undefined,
      };
      setMessages((prev) => [...prev, agentMsg]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "agent", text: "Sorry, something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="bg-white border-b border-[#e0d9cf] px-5 py-4">
        <h2 className="font-serif text-[#1a1714] text-base tracking-tight">Property Concierge</h2>
        <div className="flex items-center gap-2 mt-0.5">
          <div className="w-1.5 h-1.5 bg-[#c8a97e] rounded-full animate-gentle-pulse" />
          <p className="text-xs text-[#8a8279] font-sans">Ready to assist</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-1 bg-[#faf8f5]">
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        {loading && (
          <div className="flex justify-start mb-3">
            <div className="bg-white border border-[#e0d9cf] px-4 py-3 rounded-sm rounded-bl-none">
              <div className="flex gap-1.5">
                <span className="w-1.5 h-1.5 bg-[#c8a97e] rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-1.5 h-1.5 bg-[#c8a97e] rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-1.5 h-1.5 bg-[#c8a97e] rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-[#e0d9cf] bg-white p-3">
        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2.5 bg-[#faf8f5] border border-[#e0d9cf] rounded-sm text-sm font-sans text-[#1a1714] placeholder-[#b0a89e] focus:outline-none focus:border-[#c8a97e] transition-colors duration-300"
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-[#c8a97e] text-white px-4 py-2.5 rounded-sm text-sm font-sans font-medium hover:bg-[#a88b5e] disabled:opacity-30 disabled:cursor-not-allowed transition-colors duration-300"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
