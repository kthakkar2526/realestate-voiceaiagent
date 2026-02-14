"""
Vapi.ai webhook handler.

Vapi calls this endpoint when the voice assistant needs to execute tools
(search properties, book visits, etc.) during a call.
"""

import json
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.agent.tools import TOOL_REGISTRY

router = APIRouter(prefix="/api/vapi")


@router.post("/webhook")
async def vapi_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Vapi server messages (function calls, status updates)."""
    body = await request.json()

    # Log the full payload for debugging
    print(f"[VAPI WEBHOOK] Received: {json.dumps(body, indent=2, default=str)[:2000]}")

    message = body.get("message", {})
    msg_type = message.get("type", "")

    # Handle tool-calls from the voice assistant (Vapi sends "tool-calls" with toolCallList)
    if msg_type == "tool-calls":
        tool_call_list = message.get("toolCallList", [])
        call_id = message.get("call", {}).get("id", "voice-default")
        session_id = f"voice-{call_id}"

        results = []
        for tool_call in tool_call_list:
            tc_id = tool_call.get("id", "")
            function_info = tool_call.get("function", {})
            function_name = function_info.get("name", "")
            # arguments can be a JSON string or dict
            arguments = function_info.get("arguments", {})
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {}

            print(f"[VAPI] Tool call: {function_name}({arguments})")

            executor = TOOL_REGISTRY.get(function_name)
            if executor:
                try:
                    result = executor(db=db, session_id=session_id, **arguments)
                    print(f"[VAPI] Tool result: {json.dumps(result, default=str)[:500]}")
                    results.append({"toolCallId": tc_id, "result": json.dumps(result, default=str)})
                except Exception as e:
                    print(f"[VAPI ERROR] Tool execution failed: {e}")
                    results.append({"toolCallId": tc_id, "result": json.dumps({"error": str(e)})})
            else:
                print(f"[VAPI ERROR] Unknown function: {function_name}")
                results.append({"toolCallId": tc_id, "result": json.dumps({"error": f"Unknown function: {function_name}"})})

        return {"results": results}

    # Handle end-of-call report
    if msg_type == "end-of-call-report":
        summary = message.get("summary", "")
        call_id = message.get("call", {}).get("id", "")
        print(f"[VAPI] Call {call_id} ended. Summary: {summary}")
        return {"status": "ok"}

    # Handle other message types
    print(f"[VAPI] Unhandled message type: {msg_type}")
    return {"status": "ok"}
