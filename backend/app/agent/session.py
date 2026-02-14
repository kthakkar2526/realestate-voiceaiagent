import time


class ConversationSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history: list[dict] = []
        self.last_search_results: list[dict] = []
        self.created_at = time.time()

    def add_user_message(self, text: str):
        self.history.append({"role": "user", "parts": [{"text": text}]})

    def add_model_response(self, parts: list):
        self.history.append({"role": "model", "parts": parts})

    def add_function_response(self, name: str, response: dict):
        self.history.append({
            "role": "user",
            "parts": [{"function_response": {"name": name, "response": response}}],
        })

    def get_contents(self) -> list[dict]:
        return self.history


class SessionStore:
    def __init__(self, ttl_seconds: int = 3600):
        self._sessions: dict[str, ConversationSession] = {}
        self.ttl = ttl_seconds

    def get_or_create(self, session_id: str) -> ConversationSession:
        self._cleanup_expired()
        if session_id not in self._sessions:
            self._sessions[session_id] = ConversationSession(session_id)
        return self._sessions[session_id]

    def _cleanup_expired(self):
        now = time.time()
        expired = [k for k, v in self._sessions.items() if now - v.created_at > self.ttl]
        for k in expired:
            del self._sessions[k]


session_store = SessionStore()
