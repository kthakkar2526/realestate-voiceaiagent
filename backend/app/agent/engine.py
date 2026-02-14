from google import genai
from google.genai import types
from sqlalchemy.orm import Session as DBSession
from langfuse import Langfuse

from app.config import settings
from app.models import Lead
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import ALL_DECLARATIONS, TOOL_REGISTRY
from app.agent.session import session_store

langfuse = Langfuse(
    public_key=settings.LANGFUSE_PUBLIC_KEY,
    secret_key=settings.LANGFUSE_SECRET_KEY,
    host=settings.LANGFUSE_BASE_URL or settings.LANGFUSE_HOST,
)


class AgentResponse:
    def __init__(self, message: str, properties: list[dict] | None = None, booking: dict | None = None):
        self.message = message
        self.properties = properties
        self.booking = booking


class RealEstateAgent:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.0-flash"

    async def handle_message(self, session_id: str, user_message: str, db: DBSession, user_info: dict | None = None) -> AgentResponse:
        session = session_store.get_or_create(session_id)
        session.add_user_message(user_message)

        # Start Langfuse root span for this conversation turn
        root_span = langfuse.start_span(
            name="chat-message",
            input={"session_id": session_id, "message": user_message},
            metadata={"model": self.model, "session_id": session_id},
        )

        # Ensure lead exists
        lead = db.query(Lead).filter(Lead.session_id == session_id).first()
        if not lead:
            lead = Lead(session_id=session_id)
            db.add(lead)
            db.commit()

        # Build system prompt with user context if authenticated
        prompt = SYSTEM_PROMPT
        if user_info:
            name = user_info.get("name", "")
            phone = user_info.get("phone", "")
            email = user_info.get("email", "")
            prompt += (
                f"\n\nCURRENT USER INFO (already collected, do NOT ask again):"
                f"\n- Name: {name}"
                f"\n- Phone: {phone}"
                f"\n- Email: {email}"
                f"\nUse this info directly when booking visits or saving contacts. "
                f"Address the user by their first name."
            )

        tools = types.Tool(function_declarations=ALL_DECLARATIONS)
        config = types.GenerateContentConfig(
            tools=[tools],
            system_instruction=prompt,
            temperature=0.7,
        )

        booking_result = None
        max_iterations = 5

        for iteration in range(max_iterations):
            # Track each LLM call as a generation
            generation = langfuse.start_generation(
                name=f"gemini-call-{iteration}",
                model=self.model,
                input=session.get_contents(),
                metadata={"iteration": iteration, "session_id": session_id},
            )

            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=session.get_contents(),
                    config=config,
                )
            except Exception as e:
                generation.update(output=str(e), level="ERROR")
                generation.end()
                root_span.update(output={"error": str(e)}, level="ERROR")
                root_span.end()
                langfuse.flush()
                return AgentResponse(message="I'm sorry, I'm having trouble connecting right now. Please try again in a moment.")

            candidate = response.candidates[0]
            parts = candidate.content.parts

            # Separate function calls from text
            function_calls = [p for p in parts if p.function_call]

            if not function_calls:
                # Pure text response
                text = parts[0].text if parts and parts[0].text else "I'm here to help! What are you looking for?"
                generation.update(output=text)
                generation.end()

                session.add_model_response([{"text": text}])

                root_span.update(output={"response": text})
                root_span.end()
                langfuse.flush()

                return AgentResponse(
                    message=text,
                    properties=session.last_search_results if session.last_search_results else None,
                    booking=booking_result,
                )

            # Log the function calls Gemini wants to make
            fc_summary = [{"tool": p.function_call.name, "args": dict(p.function_call.args)} for p in function_calls]
            generation.update(output={"function_calls": fc_summary})
            generation.end()

            # Store model's function call response
            model_parts = []
            for p in parts:
                if p.function_call:
                    model_parts.append({
                        "function_call": {"name": p.function_call.name, "args": dict(p.function_call.args)}
                    })
                elif p.text:
                    model_parts.append({"text": p.text})
            session.add_model_response(model_parts)

            # Execute each function call
            for fc_part in function_calls:
                tool_name = fc_part.function_call.name
                tool_args = dict(fc_part.function_call.args)

                # Track each tool call as a span
                span = langfuse.start_span(
                    name=f"tool-{tool_name}",
                    input=tool_args,
                    metadata={"iteration": iteration, "session_id": session_id},
                )

                executor = TOOL_REGISTRY.get(tool_name)
                if not executor:
                    result = {"error": f"Unknown tool: {tool_name}"}
                    span.update(output=result, level="ERROR")
                    span.end()
                else:
                    result = executor(db=db, session_id=session_id, **tool_args)
                    span.update(output=result)
                    span.end()

                if tool_name == "search_properties":
                    session.last_search_results = result.get("properties", [])
                elif tool_name == "book_visit" and result.get("success"):
                    booking_result = result

                session.add_function_response(tool_name, result)

            # Loop continues — Gemini sees tool results next

        root_span.update(output={"warning": "Max iterations reached"}, level="WARNING")
        root_span.end()
        langfuse.flush()
        return AgentResponse(message="I apologize, I'm having trouble processing. Could you rephrase?")


agent = RealEstateAgent()
