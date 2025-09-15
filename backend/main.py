from __future__ import annotations

"""FastAPI application entry-point for the recipe chatbot."""

from pathlib import Path
from typing import Final, List, Dict, Optional
import datetime
import json
import uuid

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from openinference.instrumentation import using_session
from openinference.semconv.trace import SpanAttributes

from backend.utils import get_agent_response  # noqa: WPS433 import from parent

# Initialize Phoenix tracing
from backend.tracing import tracer

# -----------------------------------------------------------------------------
# Application setup
# -----------------------------------------------------------------------------

APP_TITLE: Final[str] = "Recipe Chatbot"
app = FastAPI(title=APP_TITLE)

# Serve static assets (currently just the HTML) under `/static/*`.
STATIC_DIR = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# -----------------------------------------------------------------------------
# Request / response models
# -----------------------------------------------------------------------------

class ChatMessage(BaseModel):
    """Schema for a single message in the chat history."""
    role: str = Field(..., description="Role of the message sender (system, user, or assistant).")
    content: str = Field(..., description="Content of the message.")

class ChatRequest(BaseModel):
    """Schema for incoming chat messages."""

    messages: List[ChatMessage] = Field(..., description="The entire conversation history.")
    session_id: Optional[str] = Field(None, description="Session identifier for conversation tracking.")


class ChatResponse(BaseModel):
    """Schema for the assistant's reply returned to the front-end."""

    messages: List[ChatMessage] = Field(..., description="The updated conversation history.")
    session_id: str = Field(..., description="Session identifier for conversation tracking.")


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:  # noqa: WPS430
    """Main conversational endpoint with Phoenix tracing.

    It proxies the user's message list to the underlying agent and returns the updated list.
    """
    # Get session ID from payload or generate a new one
    session_id = payload.session_id or str(uuid.uuid4())
    
    # Convert Pydantic models to simple dicts for the agent
    request_messages: List[Dict[str, str]] = [msg.model_dump() for msg in payload.messages]

    try:
        # Create a span for the chat turn with session context
        with tracer.start_as_current_span("chat_turn") as span:
            # Set span attributes
            span.set_attribute(SpanAttributes.SESSION_ID, session_id)
            span.set_attribute(SpanAttributes.INPUT_VALUE, str(request_messages))
            
            # Use session context to propagate session ID to child spans
            with using_session(session_id):
                updated_messages_dicts = get_agent_response(request_messages, session_id)
            
            # Set output attribute
            span.set_attribute(SpanAttributes.OUTPUT_VALUE, str(updated_messages_dicts))
            
    except Exception as exc:  # noqa: BLE001 broad; surface as HTTP 500
        # In production you would log the traceback here.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    response = ChatResponse(
        messages=[ChatMessage(**msg) for msg in updated_messages_dicts],
        session_id=session_id
    )

    # Save trace (request and response) in one place
    traces_dir = Path(__file__).parent.parent / "annotation" / "traces"
    traces_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    trace_path = traces_dir / f"trace_{ts}.json"
    with open(trace_path, "w") as f:
        json.dump({
            "request": payload.model_dump(),
            "response": response.model_dump()
        }, f)

    return response


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:  # noqa: WPS430
    """Serve the chat UI."""

    html_path = STATIC_DIR / "index.html"
    if not html_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Frontend not found. Did you forget to build it?",
        )

    return HTMLResponse(html_path.read_text(encoding="utf-8")) 