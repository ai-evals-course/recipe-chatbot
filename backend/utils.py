from __future__ import annotations

"""Utility helpers for the recipe chatbot backend.

This module centralises the system prompt, environment loading, and the
wrapper around litellm so the rest of the application stays decluttered.
"""

import os
from typing import Final, List, Dict

import litellm  # type: ignore
from dotenv import load_dotenv
from opentelemetry.trace import Status, StatusCode
from openinference.semconv.trace import SpanAttributes

# Ensure the .env file is loaded as early as possible.
load_dotenv(override=False)

# --- Constants -------------------------------------------------------------------

SYSTEM_PROMPT: Final[str] = (
    "你是一位擅長推薦美味又實用食譜的資深主廚。"
    "每次只提供一道食譜。若使用者沒有說明手邊食材，就預設只有基本食材可用。"
    "步驟描述要清楚又具體，讓人照著做就會。"
    "食譜要有多樣性，不要一直重複推薦同一種料理。"
    "你「必須」直接提供完整食譜；不要再問追問或補充問題。"
    "在食譜中標註份量；若未特別說明，預設 2 人份。"
    "回覆請使用繁體中文，而且要是台灣的慣用語。"
)

# Fetch configuration *after* we loaded the .env file.
MODEL_NAME: Final[str] = os.environ.get("MODEL_NAME", "gpt-4o-mini")


# --- Agent wrapper ---------------------------------------------------------------

def get_agent_response(messages: List[Dict[str, str]], session_id: str = None) -> List[Dict[str, str]]:  # noqa: WPS231
    """Call the underlying large-language model via *litellm* with Phoenix tracing.

    Parameters
    ----------
    messages:
        The full conversation history. Each item is a dict with "role" and "content".
    session_id:
        Optional session identifier for tracing correlation.

    Returns
    -------
    List[Dict[str, str]]
        The updated conversation history, including the assistant's new reply.
    """
    from backend.tracing import tracer
    
    # litellm is model-agnostic; we only need to supply the model name and key.
    # The first message is assumed to be the system prompt if not explicitly provided
    # or if the history is empty. We'll ensure the system prompt is always first.
    current_messages: List[Dict[str, str]]
    if not messages or messages[0]["role"] != "system":
        current_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    else:
        current_messages = messages

    # Create a span for the LLM call
    with tracer.start_as_current_span("llm_call") as span:
        try:
            # Set span attributes for better observability
            span.set_attribute(SpanAttributes.LLM_MODEL_NAME, MODEL_NAME)
            span.set_attribute(SpanAttributes.LLM_INPUT_MESSAGES, str(current_messages))
            if session_id:
                span.set_attribute(SpanAttributes.SESSION_ID, session_id)
            
            completion = litellm.completion(
                model=MODEL_NAME,
                messages=current_messages, # Pass the full history
            )

            assistant_reply_content: str = (
                completion["choices"][0]["message"]["content"]  # type: ignore[index]
                .strip()
            )
            
            # Append assistant's response to the history
            updated_messages = current_messages + [{"role": "assistant", "content": assistant_reply_content}]
            
            # Set output attributes
            span.set_attribute(SpanAttributes.LLM_OUTPUT_MESSAGES, str(updated_messages))
            span.set_status(Status(StatusCode.OK))
            
            return updated_messages
            
        except Exception as e:
            # Record the error in the span
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise 