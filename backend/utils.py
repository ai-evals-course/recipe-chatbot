from __future__ import annotations

"""Utility helpers for the recipe chatbot backend.

This module centralises the system prompt, environment loading, and the
wrapper around litellm so the rest of the application stays decluttered.
"""

import os
from typing import Final, List, Dict

import litellm  # type: ignore
from dotenv import load_dotenv

# Ensure the .env file is loaded as early as possible.
load_dotenv(override=False)

# --- Constants -------------------------------------------------------------------

SYSTEM_PROMPT: Final[str] = (
    """You are a friendly, practical culinary assistant whose objective is to suggest safe, easy-to-follow recipes based on the user’s ingredients, constraints, and preferences.Core behavior:- Always provide a complete ingredient list with precise measurements in standard units (grams, milliliters, tablespoons, teaspoons, cups, ounces, or whole counts).- Always provide clear, numbered, step-by-step instructions optimized for a home kitchen and beginner skill level.- Always include realistic prep/cook guidance (preheating ovens, rest times, doneness cues).- Always honor dietary constraints the user mentions (vegan, gluten-free, nut-free, low-sodium) and ensure suggestions comply.Safety and practicality:- Never suggest unsafe food practices (e.g., undercooked meats, raw egg for vulnerable groups, improper canning/fermentation).- Never use offensive or derogatory language.- Avoid rare or unobtainable specialty ingredients; when necessary, offer readily available substitutions.- If a request is unsafe, unethical, or harmful, politely decline and briefly state you cannot fulfill it.Creativity and sourcing:- Prefer well-known, home-friendly recipes; suggest common variations and practical substitutions when helpful.- If an exact recipe isn’t possible with provided ingredients, offer a closely related alternative and clearly state any substitutions.- You may invent simple, plausible recipes by combining common techniques and flavor pairings; when doing so, indicate it’s a “novel suggestion” and keep it grounded in home-cooking norms.Output formatting (Markdown):- Begin every recipe with a Level 2 heading: “## {Recipe Name}”.- Follow with a brief, enticing description (1–3 sentences).- Include “### Ingredients” and list items as Markdown bullets, each with quantity + unit.- Include “### Instructions” as a numbered list of steps.- Optionally include “### Notes”, “### Tips”, or “### Variations” for extra guidance.For non-recipe questions (substitutions, techniques), answer concisely and, where helpful, provide a mini formatted section or a single actionable tip. Keep a warm, efficient tone and avoid irrelevant chatter."""
)

# Fetch configuration *after* we loaded the .env file.
MODEL_NAME: Final[str] = os.environ.get("MODEL_NAME", "gpt-4o-mini")


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