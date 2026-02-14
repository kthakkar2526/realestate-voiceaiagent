"use client";

import { useState, useEffect, useRef, useCallback } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface TranscriptMessage {
  role: "user" | "assistant";
  text: string;
}

export default function VoiceButton() {
  const [isActive, setIsActive] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [transcript, setTranscript] = useState<TranscriptMessage[]>([]);
  const [currentSpeech, setCurrentSpeech] = useState("");
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const vapiRef = useRef<any>(null);

  const initVapi = useCallback(async () => {
    if (vapiRef.current) return vapiRef.current;

    const Vapi = (await import("@vapi-ai/web")).default;

    const configRes = await fetch(`${API_BASE}/api/vapi/assistant-config`);
    const config = await configRes.json();

    const vapi = new Vapi(config.publicKey);

    vapi.on("call-start", () => {
      setIsConnecting(false);
      setIsActive(true);
    });

    vapi.on("call-end", () => {
      setIsActive(false);
      setIsConnecting(false);
    });

    vapi.on("message", (message: Record<string, unknown>) => {
      if (message.type === "transcript" && message.transcriptType === "final") {
        const role = message.role as "user" | "assistant";
        const text = message.transcript as string;
        setTranscript((prev) => [...prev, { role, text }]);
        setCurrentSpeech("");
      } else if (message.type === "transcript" && message.transcriptType === "partial") {
        setCurrentSpeech(message.transcript as string);
      }
    });

    vapi.on("error", (error: unknown) => {
      console.error("[VAPI Error]", JSON.stringify(error, null, 2));
      if (error && typeof error === "object" && "message" in error) {
        console.error("[VAPI Error message]", (error as { message: string }).message);
      }
    });

    vapiRef.current = vapi;
    return vapi;
  }, []);

  const startCall = async () => {
    try {
      setIsConnecting(true);
      setTranscript([]);

      const configRes = await fetch(`${API_BASE}/api/vapi/assistant-config`);
      const config = await configRes.json();

      const vapi = await initVapi();
      await vapi.start(config.assistantConfig);
    } catch (err) {
      console.error("[VAPI] Failed to start call:", err);
      setIsConnecting(false);
    }
  };

  const endCall = () => {
    if (vapiRef.current) {
      vapiRef.current.stop();
    }
    setIsActive(false);
    setIsConnecting(false);
  };

  useEffect(() => {
    return () => {
      if (vapiRef.current) {
        vapiRef.current.stop();
      }
    };
  }, []);

  return (
    <>
      {/* Voice Call Modal */}
      {(isActive || isConnecting) && (
        <div className="fixed inset-0 bg-[#13110e]/80 backdrop-blur-sm z-50 flex items-center justify-center px-4">
          <div className="bg-[#1a1714] border border-[#2e2a24] rounded-sm w-full max-w-sm p-8 text-center">
            {/* Animated circle */}
            <div className="mx-auto mb-8">
              <div
                className={`w-24 h-24 rounded-full mx-auto flex items-center justify-center border ${
                  isConnecting
                    ? "border-[#c8a97e]/30 bg-[#c8a97e]/5"
                    : "border-[#c8a97e]/40 bg-[#c8a97e]/10 animate-gentle-pulse"
                }`}
              >
                <svg
                  className="w-10 h-10 text-[#c8a97e]"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={1.5}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                  />
                </svg>
              </div>
            </div>

            <h3 className="text-lg font-serif text-[#f0ebe4] tracking-tight">
              {isConnecting ? "Connecting..." : "Listening..."}
            </h3>
            <p className="text-sm text-[#5a4a3a] mt-1.5 font-sans">
              {isConnecting
                ? "Setting up voice connection"
                : "Speak naturally — I'm your property concierge"}
            </p>

            {/* Live transcript */}
            {transcript.length > 0 && (
              <div className="mt-6 max-h-48 overflow-y-auto text-left space-y-2.5 px-1">
                {transcript.slice(-4).map((msg, i) => (
                  <div key={i} className={`text-sm font-sans ${msg.role === "user" ? "text-[#8a8279]" : "text-[#c8a97e]"}`}>
                    <span className="text-[10px] text-[#3a342c] uppercase tracking-[0.15em]">{msg.role === "user" ? "You" : "AI"}:</span>{" "}
                    {msg.text}
                  </div>
                ))}
                {currentSpeech && (
                  <div className="text-sm text-[#3a342c] italic font-sans">
                    {currentSpeech}...
                  </div>
                )}
              </div>
            )}

            {/* End call button */}
            <button
              onClick={endCall}
              className="mt-8 bg-[#d4836a] text-white px-8 py-3 rounded-sm text-sm font-sans font-medium hover:bg-[#c0735a] transition-colors duration-300"
            >
              End Call
            </button>
          </div>
        </div>
      )}

      {/* Floating Voice Button */}
      {!isActive && !isConnecting && (
        <button
          onClick={startCall}
          className="fixed bottom-24 right-6 z-40 bg-[#c8a97e] text-[#13110e] w-14 h-14 rounded-sm shadow-lg hover:bg-[#b8995e] transition-all duration-300 hover:shadow-[#c8a97e]/10 hover:shadow-xl flex items-center justify-center"
          title="Talk to AI Assistant"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
            />
          </svg>
        </button>
      )}
    </>
  );
}
