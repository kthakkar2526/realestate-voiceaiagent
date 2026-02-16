"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const { sendOtp, verifyOtp, updateProfile, user, profileComplete } = useAuth();

  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [step, setStep] = useState<"phone" | "otp" | "profile">("phone");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user && profileComplete) {
      router.replace("/");
    } else if (user && !profileComplete) {
      setStep("profile");
    }
  }, [user, profileComplete, router]);

  const handleSendOtp = async () => {
    setError("");
    const cleaned = phone.replace(/\s/g, "");
    if (cleaned.length < 10) {
      setError("Enter a valid phone number");
      return;
    }
    setLoading(true);
    try {
      await sendOtp(cleaned);
      setStep("otp");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to send OTP");
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async () => {
    setError("");
    if (otp.length !== 6) {
      setError("Enter the 6-digit OTP");
      return;
    }
    setLoading(true);
    try {
      await verifyOtp(phone.replace(/\s/g, ""), otp);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Invalid OTP");
    } finally {
      setLoading(false);
    }
  };

  const handleProfile = async () => {
    setError("");
    if (!name.trim()) {
      setError("Name is required");
      return;
    }
    if (!email.trim() || !email.includes("@")) {
      setError("Enter a valid email");
      return;
    }
    setLoading(true);
    try {
      await updateProfile(name.trim(), email.trim());
      router.replace("/");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to save profile");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#faf8f5] flex items-center justify-center px-4 grain">
      {/* Warm ambient glow */}
      <div className="fixed top-1/3 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-[#c8a97e]/8 rounded-full blur-[150px] pointer-events-none" />

      <div className="w-full max-w-sm relative">
        {/* Logo */}
        <div className="text-center mb-10 animate-fade-up">
          <div className="w-12 h-12 border border-[#c8a97e] rounded-sm flex items-center justify-center mx-auto mb-5">
            <svg className="w-6 h-6 text-[#c8a97e]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </div>
          <h1 className="text-2xl font-serif text-[#1a1714] tracking-tight">PropertyAI</h1>
          <p className="text-[#8a8279] mt-2 text-sm font-sans">Your AI-powered real estate concierge</p>
        </div>

        {/* Card */}
        <div className="bg-white border border-[#e0d9cf] rounded-sm p-7 shadow-sm animate-fade-up delay-100">
          {step === "phone" && (
            <>
              <h2 className="text-lg font-serif text-[#1a1714] mb-1">Sign in</h2>
              <p className="text-sm text-[#8a8279] mb-7 font-sans">
                Enter your phone number to receive a verification code
              </p>
              <div className="space-y-5">
                <div>
                  <label className="block text-xs font-sans font-medium text-[#8a8279] mb-2 uppercase tracking-[0.15em]">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSendOtp()}
                    placeholder="+1 716 617 8146"
                    className="w-full px-4 py-3 bg-[#faf8f5] border border-[#e0d9cf] rounded-sm text-sm font-sans text-[#1a1714] placeholder-[#b0a89e] focus:outline-none focus:border-[#c8a97e] transition-colors duration-300"
                    disabled={loading}
                  />
                </div>
                {error && <p className="text-[#d4836a] text-sm font-sans">{error}</p>}
                <button
                  onClick={handleSendOtp}
                  disabled={loading}
                  className="w-full bg-[#c8a97e] text-white py-3 rounded-sm text-sm font-sans font-medium tracking-wide hover:bg-[#a88b5e] disabled:opacity-50 transition-colors duration-300"
                >
                  {loading ? "Sending..." : "Send OTP"}
                </button>
              </div>
            </>
          )}

          {step === "otp" && (
            <>
              <h2 className="text-lg font-serif text-[#1a1714] mb-1">Enter OTP</h2>
              <p className="text-sm text-[#8a8279] mb-7 font-sans">
                We sent a 6-digit code to <span className="text-[#1a1714] font-medium">{phone}</span>
              </p>
              <div className="space-y-5">
                <div>
                  <label className="block text-xs font-sans font-medium text-[#8a8279] mb-2 uppercase tracking-[0.15em]">
                    Verification Code
                  </label>
                  <input
                    type="text"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))}
                    onKeyDown={(e) => e.key === "Enter" && handleVerifyOtp()}
                    placeholder="123456"
                    className="w-full px-4 py-3 bg-[#faf8f5] border border-[#e0d9cf] rounded-sm text-sm text-center tracking-[0.4em] font-mono text-[#1a1714] placeholder-[#b0a89e] focus:outline-none focus:border-[#c8a97e] transition-colors duration-300"
                    disabled={loading}
                    autoFocus
                  />
                </div>
                {error && <p className="text-[#d4836a] text-sm font-sans">{error}</p>}
                <button
                  onClick={handleVerifyOtp}
                  disabled={loading}
                  className="w-full bg-[#c8a97e] text-white py-3 rounded-sm text-sm font-sans font-medium tracking-wide hover:bg-[#a88b5e] disabled:opacity-50 transition-colors duration-300"
                >
                  {loading ? "Verifying..." : "Verify & Continue"}
                </button>
                <button
                  onClick={() => { setStep("phone"); setOtp(""); setError(""); }}
                  className="w-full text-[#8a8279] text-sm font-sans hover:text-[#a88b5e] transition-colors duration-300"
                >
                  Change phone number
                </button>
              </div>
            </>
          )}

          {step === "profile" && (
            <>
              <h2 className="text-lg font-serif text-[#1a1714] mb-1">Complete your profile</h2>
              <p className="text-sm text-[#8a8279] mb-7 font-sans">
                Tell us a bit about yourself so we can assist you better
              </p>
              <div className="space-y-5">
                <div>
                  <label className="block text-xs font-sans font-medium text-[#8a8279] mb-2 uppercase tracking-[0.15em]">
                    Full Name
                  </label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleProfile()}
                    placeholder="John Doe"
                    className="w-full px-4 py-3 bg-[#faf8f5] border border-[#e0d9cf] rounded-sm text-sm font-sans text-[#1a1714] placeholder-[#b0a89e] focus:outline-none focus:border-[#c8a97e] transition-colors duration-300"
                    disabled={loading}
                    autoFocus
                  />
                </div>
                <div>
                  <label className="block text-xs font-sans font-medium text-[#8a8279] mb-2 uppercase tracking-[0.15em]">
                    Email Address
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleProfile()}
                    placeholder="john@example.com"
                    className="w-full px-4 py-3 bg-[#faf8f5] border border-[#e0d9cf] rounded-sm text-sm font-sans text-[#1a1714] placeholder-[#b0a89e] focus:outline-none focus:border-[#c8a97e] transition-colors duration-300"
                    disabled={loading}
                  />
                </div>
                {error && <p className="text-[#d4836a] text-sm font-sans">{error}</p>}
                <button
                  onClick={handleProfile}
                  disabled={loading}
                  className="w-full bg-[#c8a97e] text-white py-3 rounded-sm text-sm font-sans font-medium tracking-wide hover:bg-[#a88b5e] disabled:opacity-50 transition-colors duration-300"
                >
                  {loading ? "Saving..." : "Get Started"}
                </button>
              </div>
            </>
          )}
        </div>

        {step !== "profile" && (
          <p className="text-center text-xs text-[#b0a89e] mt-8 font-sans tracking-wide">
            OTP will be sent to your phone via SMS
          </p>
        )}
      </div>
    </div>
  );
}
