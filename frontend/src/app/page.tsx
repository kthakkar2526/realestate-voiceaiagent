"use client";

import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import ChatWidget from "@/components/chat/ChatWidget";
import VoiceButton from "@/components/voice/VoiceButton";

export default function Home() {
  const { user, loading, logout, profileComplete } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.replace("/login");
    } else if (!loading && user && !profileComplete) {
      router.replace("/login");
    }
  }, [loading, user, profileComplete, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#13110e]">
        <div className="text-center">
          <div className="w-10 h-10 border-2 border-[#c8a97e] border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="mt-4 text-[#c8a97e] text-sm font-sans tracking-wide">Loading</p>
        </div>
      </div>
    );
  }

  if (!user) return null;

  return (
    <div className="min-h-screen bg-[#13110e] text-[#f0ebe4] grain">
      {/* Nav */}
      <nav className="border-b border-[#2e2a24]">
        <div className="max-w-7xl mx-auto px-8 py-5 flex justify-between items-center">
          <div className="flex items-center gap-3 animate-fade-in">
            <div className="w-9 h-9 border border-[#c8a97e] rounded-sm flex items-center justify-center">
              <svg className="w-4.5 h-4.5 text-[#c8a97e]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
            </div>
            <span className="text-lg font-serif tracking-wide">PropertyAI</span>
          </div>
          <div className="flex items-center gap-8 animate-fade-in delay-200">
            <span className="text-sm text-[#8a8279] tracking-wide">
              {user.name || user.phone}
            </span>
            <a href="/admin" className="text-sm text-[#8a8279] hover:text-[#c8a97e] transition-colors duration-300 tracking-wide">
              Admin
            </a>
            <button onClick={logout} className="text-sm text-[#5a4a3a] hover:text-[#c8a97e] transition-colors duration-300 tracking-wide">
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Warm gradient atmosphere */}
        <div className="absolute inset-0 bg-gradient-to-b from-[#c8a97e]/8 via-transparent to-transparent" />
        <div className="absolute top-16 left-1/3 w-[500px] h-[500px] bg-[#c8a97e]/5 rounded-full blur-[120px]" />
        <div className="absolute top-32 right-1/4 w-80 h-80 bg-[#8b6f47]/5 rounded-full blur-[100px]" />

        <div className="relative max-w-7xl mx-auto px-8 pt-24 pb-20">
          <div className="text-center max-w-4xl mx-auto">
            {/* Status pill */}
            <div className="inline-flex items-center gap-2.5 border border-[#2e2a24] rounded-full px-5 py-2 mb-10 animate-fade-up">
              <div className="w-1.5 h-1.5 bg-[#c8a97e] rounded-full animate-gentle-pulse" />
              <span className="text-xs text-[#8a8279] uppercase tracking-[0.2em] font-sans">AI Concierge Active</span>
            </div>

            <h1 className="font-serif text-5xl md:text-7xl leading-[1.1] tracking-tight animate-fade-up delay-100">
              Discover Your
              <br />
              <span className="italic text-[#c8a97e]">Perfect Address</span>
            </h1>

            <p className="mt-8 text-lg text-[#8a8279] max-w-xl mx-auto leading-relaxed font-sans animate-fade-up delay-200">
              Speak or type — our AI concierge finds properties tailored to your vision,
              books visits, and handles every detail seamlessly.
            </p>

            <div className="flex justify-center gap-5 mt-12 animate-fade-up delay-300">
              <button
                onClick={() => {
                  const voiceBtn = document.querySelector("[title='Talk to AI Assistant']") as HTMLButtonElement;
                  voiceBtn?.click();
                }}
                className="group bg-[#c8a97e] hover:bg-[#b8995e] text-[#13110e] px-8 py-3.5 rounded-sm font-sans font-medium text-sm tracking-wide flex items-center gap-3 transition-all duration-300"
              >
                <svg className="w-4.5 h-4.5 transition-transform duration-300 group-hover:scale-110" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
                Speak with AI
              </button>
              <button
                onClick={() => {
                  const chatBtn = document.querySelector(".fixed.bottom-6.right-6 button") as HTMLButtonElement;
                  chatBtn?.click();
                }}
                className="group border border-[#2e2a24] hover:border-[#c8a97e]/40 text-[#f0ebe4] px-8 py-3.5 rounded-sm font-sans text-sm tracking-wide flex items-center gap-3 transition-all duration-300 hover:bg-[#c8a97e]/5"
              >
                <svg className="w-4.5 h-4.5 text-[#8a8279] group-hover:text-[#c8a97e] transition-colors duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                Chat Instead
              </button>
            </div>
          </div>
        </div>

        {/* Decorative divider */}
        <div className="max-w-7xl mx-auto px-8">
          <div className="h-px bg-gradient-to-r from-transparent via-[#2e2a24] to-transparent" />
        </div>
      </section>

      {/* How It Works */}
      <section className="max-w-7xl mx-auto px-8 py-24">
        <div className="flex items-center gap-4 mb-16 animate-fade-up">
          <div className="h-px flex-1 bg-[#2e2a24]" />
          <h2 className="text-xs uppercase tracking-[0.3em] text-[#8a8279] font-sans">How It Works</h2>
          <div className="h-px flex-1 bg-[#2e2a24]" />
        </div>
        <div className="grid md:grid-cols-3 gap-12">
          {[
            {
              step: "01",
              title: "Share Your Vision",
              desc: "Describe your ideal home — budget, location, size, amenities. Speak naturally or type your preferences.",
              icon: (
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              ),
            },
            {
              step: "02",
              title: "Curated Matches",
              desc: "AI searches real listings and presents properties that align with your exact requirements and taste.",
              icon: (
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              ),
            },
            {
              step: "03",
              title: "Book & Confirm",
              desc: "Schedule site visits instantly. Receive confirmations via email and WhatsApp — effortless.",
              icon: (
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              ),
            },
          ].map((item, i) => (
            <div
              key={item.step}
              className={`group animate-fade-up delay-${(i + 1) * 200}`}
            >
              <div className="flex items-start gap-5">
                <div className="w-14 h-14 border border-[#2e2a24] rounded-sm flex items-center justify-center flex-shrink-0 group-hover:border-[#c8a97e]/40 transition-colors duration-500">
                  <svg className="w-5 h-5 text-[#c8a97e]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    {item.icon}
                  </svg>
                </div>
                <div>
                  <span className="text-xs text-[#5a4a3a] font-sans tracking-[0.2em]">{item.step}</span>
                  <h3 className="text-xl font-serif mt-1 tracking-tight">{item.title}</h3>
                  <p className="text-sm text-[#8a8279] mt-3 leading-relaxed font-sans">{item.desc}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Stats */}
      <section className="border-t border-b border-[#2e2a24]">
        <div className="max-w-7xl mx-auto px-8 py-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-12">
            {[
              { value: "25+", label: "Mumbai Properties" },
              { value: "<2s", label: "AI Response Time" },
              { value: "24/7", label: "Always Available" },
              { value: "100%", label: "Free to Use" },
            ].map((stat, i) => (
              <div key={stat.label} className={`text-center animate-fade-up delay-${(i + 1) * 100}`}>
                <p className="text-4xl font-serif text-[#c8a97e] tracking-tight">
                  {stat.value}
                </p>
                <p className="text-xs text-[#5a4a3a] mt-2 uppercase tracking-[0.2em] font-sans">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="max-w-7xl mx-auto px-8 py-24">
        <div className="text-center mb-16">
          <h2 className="font-serif text-3xl md:text-4xl tracking-tight animate-fade-up">Built for Modern Leasing</h2>
          <p className="text-[#8a8279] mt-4 max-w-md mx-auto font-sans animate-fade-up delay-100">
            Everything a property team needs to convert leads faster with AI
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-px bg-[#2e2a24]">
          {[
            { title: "Voice AI Agent", desc: "Natural voice conversations — like speaking to a real estate professional", tag: "Primary" },
            { title: "Chat Assistant", desc: "Text-based chat with property cards, booking confirmations, and smart follow-ups", tag: "Secondary" },
            { title: "Auto Lead Capture", desc: "Every user becomes a lead the moment they sign up — ready for follow-up", tag: "CRM" },
            { title: "Email + WhatsApp", desc: "Booking confirmations sent automatically via email and WhatsApp", tag: "Notify" },
            { title: "Smart Search", desc: "AI understands natural language — 'I want a 2BHK under 80 lakh in Thane'", tag: "AI" },
            { title: "Admin Dashboard", desc: "View leads, bookings, and properties. Track conversion pipeline.", tag: "Analytics" },
          ].map((feature, i) => (
            <div
              key={feature.title}
              className={`bg-[#13110e] p-8 group hover:bg-[#1a1714] transition-colors duration-500 animate-fade-up delay-${(i + 1) * 100}`}
            >
              <span className="text-[10px] font-sans font-medium uppercase tracking-[0.2em] text-[#c8a97e] border border-[#c8a97e]/20 px-2.5 py-1 rounded-sm">
                {feature.tag}
              </span>
              <h3 className="font-serif text-lg mt-5 tracking-tight group-hover:text-[#c8a97e] transition-colors duration-500">{feature.title}</h3>
              <p className="text-sm text-[#5a4a3a] mt-2 leading-relaxed font-sans group-hover:text-[#8a8279] transition-colors duration-500">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-[#2e2a24]">
        <div className="max-w-7xl mx-auto px-8 py-24 text-center">
          <h2 className="font-serif text-3xl md:text-4xl tracking-tight animate-fade-up">
            Ready to find your
            <span className="italic text-[#c8a97e]"> dream home</span>?
          </h2>
          <p className="text-[#5a4a3a] mt-4 font-sans animate-fade-up delay-100">Start a conversation with our AI — it takes 30 seconds.</p>
          <div className="mt-10 animate-fade-up delay-200">
            <button
              onClick={() => {
                const voiceBtn = document.querySelector("[title='Talk to AI Assistant']") as HTMLButtonElement;
                voiceBtn?.click();
              }}
              className="bg-[#c8a97e] hover:bg-[#b8995e] text-[#13110e] px-10 py-4 rounded-sm font-sans font-medium text-sm tracking-wide transition-all duration-300"
            >
              Start Voice Call
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#2e2a24] py-10">
        <div className="max-w-7xl mx-auto px-8 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 border border-[#2e2a24] rounded-sm flex items-center justify-center">
              <svg className="w-3.5 h-3.5 text-[#c8a97e]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
            </div>
            <span className="text-sm font-serif text-[#5a4a3a] tracking-wide">PropertyAI</span>
          </div>
          <p className="text-xs text-[#3a342c] tracking-wide font-sans">
            Powered by Gemini AI, Vapi.ai, Langfuse
          </p>
        </div>
      </footer>

      <VoiceButton />
      <ChatWidget />
    </div>
  );
}
