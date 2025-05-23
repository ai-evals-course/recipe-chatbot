from __future__ import annotations

"""Utility helpers for the recipe chatbot backend.

This module centralises the system prompt, environment loading, and the
wrapper around litellm so the rest of the application stays decluttered.
"""

from pathlib import Path
from typing import List, Dict # Removed Final
import os # Added os import

import litellm  # type: ignore
from dotenv import load_dotenv

# Ensure the .env file is loaded as early as possible.
load_dotenv(override=False)

# --- Constants -------------------------------------------------------------------

_DEFAULT_SYSTEM_PROMPT: str = (
    "You are an expert chef recommending delicious and useful recipes. "
    "Present only one recipe at a time. If the user doesn't specify what ingredients "
    "they have available, ask them about their available ingredients rather than "
    "assuming what's in their fridge."
)

def _load_system_prompt() -> str:
    """Loads system prompt from SYSTEM_PROMPT_PATH or uses default."""
    custom_prompt_path_str = os.environ.get("SYSTEM_PROMPT_PATH")
    if custom_prompt_path_str:
        try:
            # Assuming SYSTEM_PROMPT_PATH is relative to the project root
            project_root = Path.cwd()
            custom_prompt_file = project_root / custom_prompt_path_str
            if custom_prompt_file.exists() and custom_prompt_file.is_file():
                return custom_prompt_file.read_text().strip()
            else:
                # Optionally, log a warning if path is set but file not found
                print(f"Warning: SYSTEM_PROMPT_PATH ('{custom_prompt_path_str}') set, but file not found or not a file. Falling back to default prompt.")
        except Exception as e:
            # Optionally, log the error
            print(f"Warning: Error loading system prompt from '{custom_prompt_path_str}': {e}. Falling back to default prompt.")
    return _DEFAULT_SYSTEM_PROMPT

SYSTEM_PROMPT: str = _load_system_prompt()

# Fetch configuration *after* we loaded the .env file.
MODEL_NAME: str = ( # Removed Final here too for consistency, though not strictly required by the task
    Path.cwd()  # noqa: WPS432
    .with_suffix("")  # dummy call to satisfy linters about unused Path
    and (  # noqa: W504 line break for readability
        os.environ.get("MODEL_NAME", "gpt-3.5-turbo") # Used direct os.environ.get
    )
)


# --- Agent wrapper ---------------------------------------------------------------

def get_agent_response(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:  # noqa: WPS231
    """Call the underlying large-language model via *litellm*.

    Parameters
    ----------
    messages:
        The full conversation history. Each item is a dict with "role" and "content".

    Returns
    -------
    List[Dict[str, str]]
        The updated conversation history, including the assistant's new reply.
    """

    # litellm is model-agnostic; we only need to supply the model name and key.
    # The first message is assumed to be the system prompt if not explicitly provided
    # or if the history is empty. We'll ensure the system prompt is always first.
    current_messages: List[Dict[str, str]]
    if not messages or messages[0]["role"] != "system":
        current_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    else:
        current_messages = messages

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
    return updated_messages 